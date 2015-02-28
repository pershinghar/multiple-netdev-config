#!/usr/bin/python

#
# script to run multiple cmds on cisco
# based on python - paramiko ssh client
#
# made by pershing
# pershinghar@gmail.com
#


import argparse
import paramiko
import time
from argparse import RawTextHelpFormatter


## VARS
DEBUG=0


## Functions
def debug(msg):
    if DEBUG == 1:
        print "[ DEBUG ] "+msg

def sendCommand(conn, cmd):
    conn.send(cmd+"\n")
    time.sleep(0.1)
    output = conn.recv(5000)
    debug("Command: "+cmd+output)
    return output


## MAIN

# argparse

parser = argparse.ArgumentParser(description="""Script for mass cisco configuration

    example:
        
	    ./run-commands.py -d "123.234.56.7,10.2.3.4" -c "./cmds.txt" -u admin -p password

""", formatter_class=RawTextHelpFormatter)

parser.add_argument('-d','--devs',dest='devices',help='Devices which we send commands to, divided by commas, example: "10.1.2.3,10.2.3.4"',required=True)
parser.add_argument('-c','--cmds',dest='cmds',help='Commands to send (file)',required=True)
parser.add_argument('-u','--user',dest='user',help='SSH UserName',required=True)
parser.add_argument('-p','--pass',dest='pass',help='Password to device (plaintext)')
parser.add_argument('-k','--key',dest='key',help='Key used to ssh login (when no pass specified)')
parser.add_argument('-e','--enb',dest='enable',action='store_true',help='Use enable command <not implemented yet>')
parser.add_argument('--debug',dest='debug',action='store_true',help='debug mode')

args = vars(parser.parse_args())


# main, finally
if args['debug'] == True:
    DEBUG = 1

if not args['pass'] and not args['key']:
    print "[ ERR ] No password or key specified"
    exit(2)

devices = args['devices'].split(',')

for device in devices:

    debug("Starting SSH Client")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if args['key']:
        debug("ssh connect\ndev:"+device+"\nuser:"+args['user']+'\npass:'+ args['pass'])
        ssh.load_system_host_keys(args['key'])
        ssh.connect(device,username=args['user'], look_for_keys=True)
    else:
        debug("ssh connect\n\n\tdev:"+device+"\n\tuser:"+args['user']+'\n\tpass:'+ args['pass']+"\n")
        ssh.connect(device,username=args['user'], password=args['pass'], allow_agent=False, look_for_keys=False)
    debug("Connected to "+device+", invoking shell")
    conn = ssh.invoke_shell()
    
    with open(args['cmds']) as cmdsfile:
        for cmd in cmdsfile:
            sendCommand(conn, cmd)



