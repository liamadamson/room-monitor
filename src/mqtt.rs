use super::ReadingSender;
use paho_mqtt as mqtt;
use serde_json;
use std::thread::sleep;
use std::time::Duration;

const INIT_CONNECT_RETRY_DELAY_S: u64 = 5;

pub struct MQTTReadingsSender {
    client: mqtt::Client,
    topic: String,
}

impl MQTTReadingsSender {
    pub fn new(
        server_uri: &str,
        client_id: &str,
        topic: &str,
        ca_path: &str,
        key_store_path: &str,
        private_key_path: &str,
    ) -> anyhow::Result<Self> {
        let client = Self::create_mqtt_client(server_uri, client_id)?;
        let conn_opts = Self::get_connection_opts(ca_path, key_store_path, private_key_path)?;

        loop {
            match client.connect(conn_opts.clone()) {
                Ok(_) => {
                    log::info!("Connected to MQTT broker.");

                    return Ok(Self {
                        client,
                        topic: topic.to_string(),
                    });
                }
                Err(e) => {
                    log::warn!("Failed to connect to broker: {}", e,);
                    sleep(Duration::from_secs(INIT_CONNECT_RETRY_DELAY_S));
                    log::info!("Retrying in {} seconds.", INIT_CONNECT_RETRY_DELAY_S);
                }
            }
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
        ca_path: &str,
        key_store_path: &str,
        private_key_path: &str,
    ) -> Result<mqtt::ConnectOptions, mqtt::Error> {
        let ssl_opts = mqtt::SslOptionsBuilder::new()
            .trust_store(ca_path)?
            .key_store(key_store_path)?
            .private_key(private_key_path)?
            .finalize();

        Ok(mqtt::ConnectOptionsBuilder::new()
            .ssl_options(ssl_opts)
            .finalize())
    }
}

const MQTT_QOS: i32 = 1; // At least once.

impl ReadingSender for MQTTReadingsSender {
    fn send_reading<T: serde::Serialize>(&self, reading: &T) -> anyhow::Result<()> {
        let payload = serde_json::to_string(reading)
            .map_err(|e| anyhow::anyhow!("Failed to serialize readings to JSON: {}", e))?;

        let msg = mqtt::MessageBuilder::new()
            .topic(&self.topic)
            .payload(payload)
            .qos(MQTT_QOS)
            .finalize();

        if !self.client.is_connected() {
            log::info!("MQTT client not connected. Trying to reconnect.");

            match self.client.reconnect() {
                Ok(_) => log::info!("MQTT client reconnected."),
                Err(e) => {
                    log::warn!("Failed to reconnect MQTT client: {}", e);
                    return Err(anyhow::anyhow!("Failed to reconnect MQTT client"));
                }
            }
        }

        if let Err(e) = self.client.publish(msg) {
            return Err(anyhow::anyhow!("Failed to publish MQTT message: {}", e));
        }

        Ok(())
    }
}
