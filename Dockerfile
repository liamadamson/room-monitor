FROM rust:latest as builder
WORKDIR /usr/src/myapp
COPY . .
RUN cargo install --path .

FROM debian
COPY --from=builder /usr/local/cargo/bin/room-monitor /usr/local/bin/room-monitor
CMD ["room-monitor"]