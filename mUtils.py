#!/usr/bin/python
#coding=utf-8
import paramiko
import re
def get_ssh_client(hostName,port,userName,password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostName, port, userName, password)
    except:
        print("获取*****连接失败")
        #exit()
    else:
        print("获取*****连接成功")
        return client
def sshExcommand(client,command):
    stdin, stdout, stderr = client.exec_command(command)
    lines=stdout.readlines()
    return lines
def getCpu(client):
    cpu_message = sshExcommand(client,"top -n -1 |grep 'CPU'")
    cpu_values = re.findall("(\d+\.\d*%)",",".join(cpu_message))
    return cpu_values
def getMem(client):
    mem_message = sshExcommand(client,"cat /proc/meminfo")
    mem_values = re.findall("(\d+)", ",".join(mem_message))
    return mem_values
def sshClose(client):
    client.close()