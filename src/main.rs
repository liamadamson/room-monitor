pub mod driver;

use driver::{get_bme280_driver, BME280Driver};
use std::env;
use std::thread::sleep;
use std::time::Duration;

const DEFAULT_MEASUREMENT_RATE_S: u64 = 5 * 60; // 5 minutes.

fn main() {
    setup_logging();

    log::info!("Application started");

    let measurement_rate_s = get_measurement_rate();

    let driver = get_bme280_driver().expect("Failed to get BME280 driver");
    let mut runner = Runner::new(driver);

    loop {
        if let Err(e) = runner.step() {
            log::error!("Error steppinf runner: {}", e);
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

struct Runner<T>
where
    T: BME280Driver,
{
    driver: T,
}

impl<T> Runner<T>
where
    T: BME280Driver,
{
    fn new(driver: T) -> Self {
        Self { driver }
    }

    fn step(&mut self) -> anyhow::Result<()> {
        let readings = self.driver.read()?;
        log::info!(
            "{} degC,\t {} hPa,\t {} %",
            readings.temperature,
            readings.pressure,
            readings.humidity
        );
        Ok(())
    }
}
