#Get Local IP Address
from netifaces import ifaddresses, AF_INET
LocalIP = ifaddresses('wlp7s0').setdefault(AF_INET)[0]['addr']
print(LocalIP)


#PING
import subprocess
ping_response = subprocess.Popen(["/bin/ping", "-c1", "-w100", LocalIP], stdout=subprocess.PIPE).stdout.read()
print(ping_response.decode())