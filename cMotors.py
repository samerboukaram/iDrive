import iServer

while True:
    Client = iServer.Client('192.168.43.86',3000)
    Client.Send('3000')
