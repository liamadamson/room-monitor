FROM rust:latest as builder
WORKDIR /usr/src/myapp
COPY . .

# Required for Paho MQTT
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libssl-dev build-essential cmake

RUN cargo install --path .

FROM debian

COPY --from=builder /usr/local/cargo/bin/room-monitor /usr/local/bin/room-monitor

# Required for Paho MQTT
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libssl-dev

CMD ["room-monitor"]