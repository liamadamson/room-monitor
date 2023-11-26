use super::ReadingsSender;
use paho_mqtt as mqtt;
use serde_json;

pub struct MQTTReadingsSender {
    client: mqtt::Client,
    topic: String,
}

impl MQTTReadingsSender {
    pub fn new(
        server_uri: &str,
        client_id: &str,
        topic: &str,
        ca_file: &str,
        key_store_file: &str,
        private_key_file: &str,
    ) -> anyhow::Result<Self> {
        match Self::create_mqtt_client(server_uri, client_id) {
            Ok(client) => {
                match Self::get_connection_opts(ca_file, key_store_file, private_key_file) {
                    Ok(connection_opts) => loop {
                        match client.connect(connection_opts.clone()) {
                            Ok(_) => {
                                log::info!("Connected to MQTT broker");

                                return Ok(Self {
                                    client,
                                    topic: topic.to_string(),
                                });
                            }
                            Err(e) => {
                                log::warn!(
                                    "Failed to connect to MQTT broker, retrying in 5 seconds: {}",
                                    e
                                );
                                std::thread::sleep(std::time::Duration::from_secs(5));
                            }
                        }
                    },
                    Err(e) => Err(anyhow::anyhow!(
                        "Failed to create MQTT connection options: {}",
                        e
                    )),
                }
            }
            Err(e) => Err(anyhow::anyhow!("Failed to create MQTT client: {}", e)),
        }
    }

    fn create_mqtt_client(uri: &str, client_id: &str) -> Result<mqtt::Client, mqtt::Error> {
        let opts = mqtt::CreateOptionsBuilder::new_v3()
            .server_uri(uri)
            .client_id(client_id)
            .finalize();

        mqtt::Client::new(opts)
    }

    pub fn get_connection_opts(
        ca_file: &str,
        key_store_file: &str,
        private_key_file: &str,
    ) -> Result<mqtt::ConnectOptions, mqtt::Error> {
        let ssl_opts = mqtt::SslOptionsBuilder::new()
            .trust_store(ca_file)?
            .key_store(key_store_file)?
            .private_key(private_key_file)?
            .finalize();

        Ok(mqtt::ConnectOptionsBuilder::new()
            .ssl_options(ssl_opts)
            .finalize())
    }
}

impl ReadingsSender for MQTTReadingsSender {
    fn send_readings(&self, readings: &crate::driver::Readings) -> anyhow::Result<()> {
        let payload = serde_json::to_string(readings).unwrap();

        let msg = mqtt::MessageBuilder::new()
            .topic(&self.topic)
            .payload(payload)
            .qos(1)
            .finalize();

        if !self.client.is_connected() {
            log::info!("MQTT client is not connected, trying to reconnect.");

            // Try to reconnect once.
            match self.client.reconnect() {
                Ok(_) => log::info!("MQTT client reconnected"),
                Err(e) => {
                    log::warn!("Failed to reconnect MQTT client: {}", e);
                    return Err(anyhow::anyhow!("Failed to reconnect MQTT client"));
                }
            }
        }

        match self.client.publish(msg) {
            Ok(_) => Ok(()),
            Err(e) => Err(anyhow::anyhow!("Failed to publish MQTT message: {}", e)),
        }
    }
}
