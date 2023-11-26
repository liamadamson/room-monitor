use super::{BME280Driver, Reading};
use bme280::i2c::BME280;
use linux_embedded_hal::{Delay, I2cdev};

pub struct LinuxBME280Driver {
    bme280: BME280<I2cdev>,
}

impl LinuxBME280Driver {
    pub fn new() -> anyhow::Result<Self> {
        let i2c_bus =
            I2cdev::new("/dev/i2c-1").map_err(|_| anyhow::anyhow!("Failed to open I2C bus."))?;

        let mut bme280 = BME280::new_primary(i2c_bus);
        bme280
            .init(&mut Delay)
            .map_err(|_| anyhow::anyhow!("Failed to init BME280."))?;

        Ok(Self { bme280 })
    }
}

impl BME280Driver for LinuxBME280Driver {
    fn read(&mut self) -> anyhow::Result<Reading> {
        let measurements = self
            .bme280
            .measure(&mut Delay)
            .map_err(|_| anyhow::anyhow!("Failed to read measurements."))?;

        Ok(Reading {
            temperature: measurements.temperature,
            pressure: measurements.pressure,
            humidity: measurements.humidity,
        })
    }
}
