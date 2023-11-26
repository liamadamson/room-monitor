pub mod driver;
pub mod mqtt;

use base64::Engine;
use driver::{get_bme280_driver, BME280Driver};
use mqtt::MQTTReadingsSender;
use std::env;
use std::thread::sleep;
use std::time::Duration;

const DEFAULT_MEASUREMENT_RATE_S: u64 = 5 * 60; // 5 minutes.

const TMP_AWS_ROOT_CA_FILE: &str = "/tmp/room_monitor/ca.crt";
const TMP_AWS_KEY_STORE_FILE: &str = "/tmp/room_monitor/client.pem.crt";
const TMP_AWS_PRIVATE_KEY_FILE: &str = "/tmp/room_monitor/private.pem.key";

fn main() {
    setup_logging();

    log::info!("Application started");

    let measurement_rate_s = get_measurement_rate();

    let server_uri = env::var("MQTT_SERVER_URI").expect("MQTT_SERVER_URI not set");
    let client_id = env::var("MQTT_CLIENT_ID").expect("MQTT_CLIENT_ID not set");
    let topic = env::var("MQTT_TOPIC").expect("MQTT_TOPIC not set");

    set_credential("MQTT_CA_CERT", TMP_AWS_ROOT_CA_FILE);
    set_credential("MQTT_CLIENT_CERT", TMP_AWS_KEY_STORE_FILE);
    set_credential("MQTT_PRIVATE_KEY", TMP_AWS_PRIVATE_KEY_FILE);

    let mqtt_sender = MQTTReadingsSender::new(
        &server_uri,
        &client_id,
        &topic,
        TMP_AWS_ROOT_CA_FILE,
        TMP_AWS_KEY_STORE_FILE,
        TMP_AWS_PRIVATE_KEY_FILE,
    )
    .expect("Failed to create MQTT sender");

    let driver = get_bme280_driver().expect("Failed to get BME280 driver");
    let mut runner = Runner::new(driver, mqtt_sender);

    loop {
        if let Err(e) = runner.step() {
            log::error!("Error stepping runner: {}", e);
        }

        sleep(Duration::from_secs(measurement_rate_s));
    }
}

fn get_measurement_rate() -> u64 {
    match env::var("MEASUREMENT_RATE_S") {
        Ok(rate) => match rate.parse::<u64>() {
            Ok(rate) => {
                log::info!("Using MEASUREMENT_RATE_S of {}", rate);
                rate
            }
            Err(_) => {
                log::warn!(
                    "MEASUREMENT_RATE_S is not a valid integer, using default of {}",
                    DEFAULT_MEASUREMENT_RATE_S
                );
                DEFAULT_MEASUREMENT_RATE_S
            }
        },
        Err(_) => {
            log::warn!(
                "MEASUREMENT_RATE_S not set, using default of {}",
                DEFAULT_MEASUREMENT_RATE_S
            );
            DEFAULT_MEASUREMENT_RATE_S
        }
    }
}

fn setup_logging() {
    let mut builder = env_logger::Builder::from_default_env();
    builder
        .filter_level(log::LevelFilter::Debug)
        .target(env_logger::Target::Stdout)
        .init();
}

struct Runner<T, U>
where
    T: BME280Driver,
    U: ReadingsSender,
{
    driver: T,
    sender: U,
}

impl<T, U> Runner<T, U>
where
    T: BME280Driver,
    U: ReadingsSender,
{
    fn new(driver: T, sender: U) -> Self {
        Self { driver, sender }
    }

    fn step(&mut self) -> anyhow::Result<()> {
        let readings = self.driver.read()?;

        if let Err(e) = self.sender.send_readings(&readings) {
            log::warn!("Failed to send readings: {}", e);
            log::info!(
                "Unsent reading: temperature: {}, pressure: {}, humidity: {}",
                readings.temperature,
                readings.pressure,
                readings.humidity
            );
        } else {
            log::info!("Successfully sent readings");
        }

        Ok(())
    }
}

pub trait ReadingsSender {
    fn send_readings(&self, readings: &driver::Readings) -> anyhow::Result<()>;
}

fn set_credential(env_var: &str, file_name: &str) {
    match env::var(env_var) {
        Ok(val) => {
            // Write the contents of base64-encoded env var to a file.
            let engine = base64::engine::general_purpose::STANDARD;
            match engine.decode(val) {
                Ok(decoded) => {
                    // Create the directory if it doesn't exist.
                    if let Some(parent) = std::path::Path::new(file_name).parent() {
                        if !parent.exists() {
                            if let Err(e) = std::fs::create_dir_all(parent) {
                                log::error!(
                                    "Failed to create directory {}: {}",
                                    parent.display(),
                                    e
                                );
                                std::process::exit(1);
                            }
                        }
                    }

                    if let Err(e) = std::fs::write(file_name, decoded) {
                        log::error!("Failed to write {} to {}: {}", env_var, file_name, e);
                        std::process::exit(1);
                    }
                }
                Err(e) => {
                    log::error!(
                        "Env variable {} is not a valid base64 string: {}",
                        env_var,
                        e
                    );
                    std::process::exit(1);
                }
            }
        }
        Err(_) => {
            log::error!("{} not set", env_var);
            std::process::exit(1);
        }
    }
}
