from dht22_monitor import monitor

app = monitor.Monitor(30.0, 4)
app.run()
