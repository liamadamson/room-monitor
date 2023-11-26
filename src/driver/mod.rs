#[cfg(target_os = "linux")]
pub mod linux;

#[cfg(target_os = "linux")]
pub fn get_bme280_driver() -> anyhow::Result<impl BME280Driver> {
    Ok(linux::LinuxBME280Driver::new()?)
}

#[cfg(not(target_os = "linux"))]
pub fn get_bme280_driver() -> anyhow::Result<impl BME280Driver> {
    let mut driver = MockBME280Driver::new();
    driver.expect_read().returning(|| {
        Ok(Readings {
            temperature: 18.5,
            pressure: 1013.25,
            humidity: 45.0,
        })
    });

    Ok(driver)
}

#[derive(serde::Serialize)]
pub struct Readings {
    pub temperature: f32,
    pub pressure: f32,
    pub humidity: f32,
}

#[mockall::automock]
pub trait BME280Driver {
    fn read(&mut self) -> anyhow::Result<Readings>;
}
