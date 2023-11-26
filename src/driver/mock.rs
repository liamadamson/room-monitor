use super::{BME280Driver, Reading};

pub struct MockBME280Driver;

impl BME280Driver for MockBME280Driver {
    fn read(&mut self) -> anyhow::Result<Reading> {
        Ok(Reading {
            temperature: 18.5,
            pressure: 1013.25,
            humidity: 45.0,
        })
    }
}
