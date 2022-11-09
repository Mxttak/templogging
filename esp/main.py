import json
# from machine import UART
import machine
import time
import network, urequests
import ujson
import dht


def do_connect():    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(config["ssid"], config["key"])
        while not wlan.isconnected():
            pass

def deep_sleep(msecs):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, msecs)
    machine.deepsleep()


# uart = UART(0, baudrate=115200)
# uart.write(f'wake up reason: {machine.reset_cause()}\n\r')

with open("config.json") as f:
    config = json.load(f) 
# uart.write(f"config:\n\r\t{config}\n\r")


d = dht.DHT11(machine.Pin(5))

do_connect()
# uart.write(f"connected to wlan")

time.sleep(1)
d.measure()
data = ujson.dumps({
    "room": config["room"], "temperature": d.temperature(), "humidity": d.humidity(),
})
# uart.write(f"data: {data}")

x = urequests.post(config["url"], headers = {'content-type': 'application/json'}, data=data)
# uart.write(f"transmission result: {x.json()}")
    
# go to sleep for 10min
deep_sleep(580000)
