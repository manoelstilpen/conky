#!/usr/bin/env python

import subprocess
import argparse

def get_battery():

	fd = open('/sys/class/power_supply/BAT1/charge_full')
	capacity = int(fd.readline())
	fd.close()

	fd = open('/sys/class/power_supply/BAT1/charge_now')
	remaining = int(fd.readline())
	fd.close()

	fd = open('/sys/class/power_supply/BAT1/status')
	status = fd.readline().lower()
	fd.close()

	percentage = int((remaining * 100) / capacity)
	# print(percentage)
	status = status.replace('\n', '')
	if 5 < percentage < 20 and status == "discharging":
		subprocess.Popen(['notify-send', '-t', '3000', '-i', 'notification-battery-low', "Alerta de Bateria", 'Ta na hora de carregar...'])
	elif percentage <= 5 and status == "discharging":
		subprocess.Popen(['notify-send', '-t', '3000', '-i', 'notification-battery-low', "BATERIA CRITICA!", 'Plugue na tomada imediatamente!'])	
		subprocess.Popen(['espeak', '-v', 'pt', "SOCORRO VOU MORRER"])		

	progress_size = 50
	block = int(round((progress_size/100)*percentage))
	text = "[{0}] {1}%".format( "|"*block + " "*(progress_size-block), percentage)

	print(text)

def get_battery_status():
	fd = open('/sys/class/power_supply/BAT1/status')
	status = fd.readline().replace('\n','').upper()
	fd.close()
	print(status)

def get_ssid():
	command = 'iwgetid -r'
	output = ((subprocess.check_output(command,shell=True).decode('UTF-8')).replace('\n',''))
	print(output)


if __name__ == "__main__":
	#ifconfig wlp2s0 | grep -w inet | awk '{print $2}'	

	parser = argparse.ArgumentParser()
	parser.add_argument('--battery', action='store_true')
	parser.add_argument('--battery_status', action='store_true')
	parser.add_argument('--ssid', action='store_true')
	arguments = parser.parse_args()
	
	if arguments.battery == True:
		get_battery()
	elif arguments.battery_status == True:
		get_battery_status()
	elif arguments.ssid == True:
		get_ssid()
