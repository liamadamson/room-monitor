pub mod driver;

use driver::{get_bme280_driver, BME280Driver};
use std::thread::sleep;
use std::time::Duration;

const LOOP_RATE_S: u64 = 5 * 60;

fn main() {
    setup_logging();

    log::info!("Application started");

    let driver = get_bme280_driver().expect("Failed to get BME280 driver");
    let mut runner = Runner::new(driver);

    loop {
        if let Err(e) = runner.step() {
            log::error!("Error steppinf runner: {}", e);
        }

        sleep(Duration::from_secs(LOOP_RATE_S));
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
