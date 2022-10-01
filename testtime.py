import time
import testtime2

print(time.time())
print('flouppy')

import multiprocessing

print(multiprocessing.cpu_count())

import platform

print(platform.system())
print(platform.version())
print(platform.node())
print(platform.processor())
# Darwin



import requests


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data


print(get_location())