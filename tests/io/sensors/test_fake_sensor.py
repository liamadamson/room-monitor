from room_monitor.io.sensors import fake_sensor

def test_fake_sensor_unit():
    fake_sensor_instance = fake_sensor.FakeSensor()
    assert fake_sensor_instance.unit == "fake unit"


def test_fake_sensor_read_increments_by_one():
    fake_sensor_instance = fake_sensor.FakeSensor()
    
    for x in range(10):
        assert fake_sensor_instance.read() == x
