import socks
import logging
from telethon.sync import TelegramClient, events

from telethon.tl.custom.button import Button
import time
import argparse
import json
import sys
import os
import time
import threading
import asyncio
import datetime

logging.basicConfig(level=logging.INFO,
	format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
	datefmt="%d-%m-%Y %H:%M:%S",
	stream=sys.stdout)

parser = argparse.ArgumentParser(description="Script create session file")

parser.add_argument(
	"-f",
	"--file",
	type = str,
	dest="file",
	help = "Input JSON file of accaunts",
	default="accaunts.json")

parser.add_argument(
	"-n",
	"--number",
	type = int,
	dest="number",
	help = "Accaunt number",
	default=0)

parser.add_argument(
	"-t",
	"--tor",
	action="store_const",
	const=True)

args = parser.parse_args()

with open(args.file, "r") as f:
    data = json.loads(f.read())

if len(data["accaunts"]) <= args.number:
	logging.info("The index went beyond")
	sys.exit(-1)

i = 0
for accaunt in data["accaunts"]:
	if i == args.number:
		break;
	i += 1

commands = {
	"none": 0,
	"new": 1,
	"wait": 2,
	"earned": 3,
	"noads": 4,
	"stay": 5,
	"choose" : 6,
	"unknown": 7
}

if args.tor:
	logging.info("Starting TOR")
	os.system("/bin/tor SOCKSPort %s ExitRelay 0 ExcludeExitNodes {ru},{ua},{by},{kz},{??} StrictNodes 1" % int(9051 + args.number))

client = TelegramClient("/home/user/workers/sessions/%s.session" % accaunt["title"], int(accaunt["api_id"]), accaunt["api_hash"], proxy=(socks.SOCKS5, "127.0.0.1", int(9051 + args.number)))

client.start()

litecoin = client.get_entity("Litecoin_click_bot")
logging.info(litecoin.id)

loop = asyncio.get_event_loop()

class Command(object):
	"""Container for received bot massages by separating by commands"""
	def __init__(self, command, message):
		self.command = command
		self.message = message

	def get_command(self):
		return self.command

	def get_message(self):
		return self.message

class Sort_commands(object):
	"""Sort commands by message.id"""
	def __init__(self):
		self.commands = []
	
	def put(self, command):
		self.commands.append(command)
		self.commands.sort(key=lambda command: command.message.id)

	def get(self):
		if len(self.commands) > 0:
			return self.commands.pop(0)

	def empty(self):
		return len(self.commands) == 0

sorted_commands = Sort_commands()

@client.on(events.NewMessage)
async def handler(event):
	sender = await event.get_sender()
	global litecoin
	if litecoin.id == sender.id:
		logging.info("New message from litecoin")
		logging.info("MESSAGE ID == %s TEXT== %s" % (event.message.id, event.message.raw_text))

		global message
		global start_command_time
		global end_command_time

		global sorted_commands

		if "Press the \"Visit website\" button to earn" in event.message.raw_text:
			logging.info("New message with link")
			#message = event.message
			sorted_commands.put(Command(commands["new"], event.message))
			start_command_time = datetime.datetime.now()
		elif "You earned" in event.message.raw_text:
			logging.info("You earned")
			sorted_commands.put(Command(commands["earned"], event.message))
			start_command_time = datetime.datetime.now()
		elif "Sorry, there are no new ads available" in event.message.raw_text:
			logging.info("No new ads")
			sorted_commands.put(Command(commands["noads"], event.message))
			start_command_time = datetime.datetime.now()
		elif "Please stay on the site" in event.message.raw_text:
			logging.info("Please stay on the site")
			sorted_commands.put(Command(commands["stay"], event.message))
			start_command_time = datetime.datetime.now()
		elif "You must stay on the site" in event.message.raw_text:
			logging.info("Please stay on the site")
			sorted_commands.put(Command(commands["stay"], event.message))
			start_command_time = datetime.datetime.now()
		elif "Choose a setting to edit below" in event.message.raw_text:
			logging.info("Choose a setting to edit below")
			sorted_commands.put(Command(commands["choose"], event.message))
			start_command_time = datetime.datetime.now()			
		else:
			logging.info("UNKNOWN COMMAND")
			sorted_commands.put(Command(commands["unknown"], event.message))
			start_command_time = datetime.datetime.now()

async def main():

	me = await client.get_me()
	
	logging.info(me.username)
	logging.info(me.phone)

	await client.send_message("Litecoin_click_bot", "Visit sites")
	timeout_flag = False
	timeout = 60
	global start_command_time
	start_command_time = datetime.datetime.now()
	global end_command_time
	end_command_time = datetime.datetime.now()

	global start_time				
	global end_time

	global sorted_commands

	cycles = 10
	cycles_count = 0

	while True:
		
		if not sorted_commands.empty():
			cycles_count = 0
			item = sorted_commands.get()

			if item.command == commands["stay"]:
				logging.info("Stay on the site")

			if item.command == commands["new"]:
				logging.info("New visit message")
				logging.info(item.message.buttons[0][0].url)
				url = item.message.buttons[0][0].url
				from selenium import webdriver
				chrome_options = webdriver.ChromeOptions()
				chrome_options.add_argument("--headless")
				chrome_options.add_argument("--window-size=1920,1080")
				chrome_options.add_argument("--disable-gpu")
				chrome_options.add_argument("--no-sandbox")
				chrome_options.add_argument("--test-type")
				chrome_options.add_argument("--disable-setuid-sandbox")
				chrome_options.add_argument("--disable-infobars")
				caps = {"browserName": "chrome", "chromeOptions": "--headless"}
				global driver

				try:
					driver.quit()
				except NameError:
					logging.info("First driver")
				except:
					logging.info("OOh My GOD")
				try:
					driver = webdriver.Remote(command_executor=f"http://localhost:4444/wd/hub", desired_capabilities=chrome_options.to_capabilities())
					driver.get(url)
					var = driver.find_elements_by_xpath("//*[contains(text(), 'reCAPTCHA')]")
				except:
					logging.info("Except xpath 199 line")
					var = "lhgiugyuig";
				
				if len(var) != 0:
					logging.info("reCAPTCHA finded %s" % len(var))
					try:
						driver.quit()
					except:
						logging.info("Except driver.quit() len(var) != 0")
					logging.info("Skipping task")
					await item.message.click(1, 1)
				else:
					logging.info("reCAPTCHA don't find")
					timeout = 70
					timeout_flag = True
					start_time = datetime.datetime.now()
					end_time = datetime.datetime.now()

			if item.command == commands["earned"]:
				try:
					driver.quit()
				except:
					logging.info("driver.quit() bag")
				
				timeout_flag = False
				logging.info("Wait new visit message")

			if item.command == commands["noads"]:
				await client.send_message("Litecoin_click_bot", "/settings")
			if item.command == commands["choose"]:
				logging.info("choose command")
				await asyncio.sleep(1)
				await item.message.click(1, 0)
				await asyncio.sleep(1)
				messages = await client.get_messages("Litecoin_click_bot", limit=1)

				await asyncio.sleep(1)

				if "✅" in messages[0].buttons[0][0].text:
					logging.info("Visiting sites was enabled. SKIP")
				else:
					logging.info("Visiting sites will be enabled!")
					await messages[0].click(0, 0)

				start_time = datetime.datetime.now()
				end_time = datetime.datetime.now()
				
				timeout_flag = True

				import random
				timeout = random.randint(120, 900)

				logging.info("Wait %s seconds" % timeout)

		else:
			if not timeout_flag:
				logging.info("!!!!!!NO COMMAND!!!!!!!! CYCLES %s" % cycles_count)
				if cycles_count > cycles:
					cycles_count = 0
					await client.send_message("Litecoin_click_bot", "Visit sites")
				cycles_count += 1
				
					
	
		if timeout_flag == True:
			logging.info("Counter %s timeout %s" % ((end_time - start_time).seconds, timeout))
			if (end_time - start_time).seconds >= timeout:
				if item.command == commands["noads"]:
				
					timeout_flag = False
					logging.info("No Ads Timout. New command")
					await client.send_message("Litecoin_click_bot", "Visit sites")
				elif item.command == commands["choose"]:

					timeout_flag = False
					logging.info("!!!!!!No Ads CHOOSE!!!!")
					await client.send_message("Litecoin_click_bot", "Visit sites")

				else:
					logging.info("Timout. Skipping task")
					try:
						driver.quit()
					except:
						logging.info("except driver again")
					try:
						await item.message.click(1, 1)
					except:
						logging.info("No button skip")
					timeout_flag = False

		await asyncio.sleep(1)
		end_time = datetime.datetime.now()

client.loop.create_task(main())
client.run_until_disconnected()