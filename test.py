#!/usr/bin/python
from mUtils import get_ssh_client,getCpu,getMem
hostName="192.168.34.162"
port=22
userName='root'
password='NSD123dev'
client=get_ssh_client(hostName,port,userName,password)
print(client)
print(getCpu(client))
print(getMem(client))