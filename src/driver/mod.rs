#[cfg(target_os = "linux")]
mod linux;
mod mock;

#[derive(serde::Serialize)]
pub struct Reading {
    pub temperature: f32,
    pub pressure: f32,
    pub humidity: f32,
}

pub trait BME280Driver {
    fn read(&mut self) -> anyhow::Result<Reading>;
}

#[cfg(target_os = "linux")]
pub fn get_bme280_driver() -> anyhow::Result<impl BME280Driver> {
    Ok(linux::LinuxBME280Driver::new()?)
}

#[cfg(not(target_os = "linux"))]
pub fn get_bme280_driver() -> anyhow::Result<impl BME280Driver> {
    Ok(mock::MockBME280Driver)
}
