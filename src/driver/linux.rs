extern crate bme280;
extern crate linux_embedded_hal as hal;

use super::{BME280Driver, Readings};

pub struct LinuxBME280Driver {
    bme280: bme280::i2c::BME280<hal::I2cdev>,
}

impl LinuxBME280Driver {
    pub fn new() -> anyhow::Result<Self> {
        match hal::I2cdev::new("/dev/i2c-1") {
            Ok(i2c_bus) => {
                let mut bme280 = bme280::i2c::BME280::new_primary(i2c_bus);
                match bme280.init(&mut hal::Delay) {
                    Ok(_) => Ok(Self { bme280 }),
                    Err(_) => Err(anyhow::anyhow!("Failed to init BME280.")),
                }
            }
            Err(_) => Err(anyhow::anyhow!("Failed to open I2C bus.")),
        }
    }
}

impl BME280Driver for LinuxBME280Driver {
    fn read(&mut self) -> anyhow::Result<Readings> {
        match self.bme280.measure(&mut hal::Delay) {
            Ok(measurements) => Ok(Readings {
                temperature: measurements.temperature,
                pressure: measurements.pressure,
                humidity: measurements.humidity,
            }),
            Err(_) => Err(anyhow::anyhow!("Failed to read measurements.")),
        }
    }
}
