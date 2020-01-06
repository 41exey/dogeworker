import socks
import logging
from telethon.sync import TelegramClient, events
#from telethon import TelegramClient, events

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

#print(args.file)
#print(args.number)

if len(data["accaunts"]) <= args.number:
	logging.info("The index went beyond")
	#print("The index went beyond")
	sys.exit(-1)

i = 0
for accaunt in data["accaunts"]:
	if i == args.number:
		break;
	i += 1

#hello = False
#exitFlag = False

commands = {
	"none": 0,
	"new": 1,
	"wait": 2,
	"earned": 3,
	"noads": 4
}

if args.tor:
	logging.info("Starting TOR")
	#print("Starting TOR")
	os.system("/bin/tor SOCKSPort %s ExitRelay 0 ExcludeExitNodes {ru},{ua},{by},{kz},{??} StrictNodes 1" % int(9051 + args.number))

client = TelegramClient("/home/user/workers/sessions/%s.session" % accaunt["title"], int(accaunt["api_id"]), accaunt["api_hash"], proxy=(socks.SOCKS5, "127.0.0.1", int(9051 + args.number)))

client.start()

#me = client.get_me()

#print(me.username, flush=True)
#print(me.phone, flush=True)

#litecoin = client.get_entity("Litecoin_click_bot")
#print(litecoin.id)
#print(litecoin)




#time.sleep(2)
#exitFlag = True

status = commands["none"]
status_double = commands["none"]
litecoin = client.get_entity("Litecoin_click_bot")
logging.info(litecoin.id)
#print(litecoin.id)

loop = asyncio.get_event_loop()

@client.on(events.NewMessage)
async def handler(event):
	sender = await event.get_sender()
	global litecoin
	if litecoin.id == sender.id:
		logging.info("New message from litecoin")
		#print("New message fron litecoin")
		logging.info(event.message.raw_text)
		#print(event.message.raw_text)
		#hello = True
		#global exitFlag
		#exitFlag = True
		global status
		global status_double
		global message
		global start_command
		global end_command
		if "Press the 'Visit website' button to earn" in event.message.raw_text:
			logging.info("New message with link")
			#print("New message with link")
			status = commands["new"]
			#print(event.message.buttons[0][0].url)
			message = event.message
			start_command = datetime.datetime.now()
		if "You earned" in event.message.raw_text:
			logging.info("You earned")
			status = commands["earned"]
			start_command = datetime.datetime.now()
		if "Sorry, there are no new ads available" in event.message.raw_text:
			logging.info("No new ads")
			status = commands["noads"]
			status_double = commands["noads"]
			start_command = datetime.datetime.now()

#client.send_message("Litecoin_click_bot", "Visit sites")

client.send_message("Litecoin_click_bot", "Visit sites")

async def main():

	me = await client.get_me()
	
	logging.info(me.username)
	#print(me.username, flush=True)
	logging.info(me.phone)
	#print(me.phone, flush=True)
	#global litecoin
	#litecoin = await client.get_entity("Litecoin_click_bot")
	#print(litecoin.id)

	await client.send_message("Litecoin_click_bot", "Visit sites")
	timeout_flag = False
	timeout = 60
	global end_command
	end_command = datetime.datetime.now()
	while True:
		global exitFlag
		global status
		if status == commands["new"]:
			status = commands["none"]
			global message
			logging.info(message.buttons[0][0].url)
			url = message.buttons[0][0].url
			#print(message.buttons[0][0].url)
########################################


			from selenium import webdriver

			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--window-size=1920,1080")
			chrome_options.add_argument("--disable-gpu")
			chrome_options.add_argument("--no-sandbox")
			chrome_options.add_argument("--test-type")
			chrome_options.add_argument("--disable-setuid-sandbox")
			chrome_options.add_argument("--disable-infobars")

#			url = "http://www.python.org"

			caps = {"browserName": "chrome", "chromeOptions": "--headless"}
			global driver

			try:
				driver.quit()
			except NameError:
				logging.info("First driver")
			except:
				logging.info("OOh My GOD")
#			if driver is None:
#				logging.info("First driver")
#			else:
#				driver.quit()

			driver = webdriver.Remote(command_executor=f"http://localhost:4444/wd/hub", desired_capabilities=chrome_options.to_capabilities())
			driver.get(url)
			var = driver.find_elements_by_xpath("//*[contains(text(), 'reCAPTCHA')]")
			if len(var) != 0:
				logging.info("reCAPTCHA finded %s" % len(var))
				#print("reCAPTCHA finded %s" % len(var))
				driver.quit()
				logging.info("Skipping task")
				await message.click(1, 1)
			else:
				logging.info("reCAPTCHA don't find")
				#print("reCAPTCHA don't find")
				timeout = 60
				timeout_flag = True
				global start				
				start = datetime.datetime.now()
				global end
				end = datetime.datetime.now()

#exit when recived message			
#driver.quit()


########################################
#			time.sleep(5)
#			loop = asyncio.new_event_loop()
#			asyncio.set_event_loop(loop)
# Here not forward
			
#			loop.close()
#			if exitFlag:
#				#threadName.exit()
#				break

		if status == commands["earned"]:
			status = commands["none"]
			#global driver
			try:
				driver.quit()
			except:
				logging.info("driver.quit() bag")
			timeout_flag = False
			logging.info("Wait new visit message")
			await client.send_message("Litecoin_click_bot", "Visit sites")

		if status == commands["noads"]:
			start = datetime.datetime.now()
			end = datetime.datetime.now()
			status = commands["none"]
			timeout_flag = True
#will add random
			import random
#			timeout = 30
			timeout = random.randint(120, 900)
			logging.info("Wait %s seconds" % timeout)

		#global end
		#global start
# We don't know this variable if don't recived now command
		if timeout_flag == True:
			logging.info("Counter %s" % (end - start).seconds)
			if (end - start).seconds >= timeout:
				#logging.info("status_double == %s" % status_double)
				global status_double			
				if status_double == commands["noads"]:
					status_double = commands["none"]
					timeout_flag = False
					logging.info("No Ads Timout. New command")
					await client.send_message("Litecoin_click_bot", "Visit sites")
					
				else:
					logging.info("Timout. Skipping task")
					#global driver
					driver.quit()
					await message.click(1, 1)
					timeout_flag = False

		global start_command
		
		if (end_command - start_command).seconds >= 120 and timeout_flag == False:
			start_command = datetime.datetime.now()
			logging.info("Many long time don't be commands")
			await client.send_message("Litecoin_click_bot", "Visit sites")
		
		logging.info("Main loop %s" % (end_command - start_command).seconds)
		#print("Main loop")
		#yield
		#time.sleep(1)
		await asyncio.sleep(1)
		#global end
		end = datetime.datetime.now()
		end_command = end

#client.loop.create_task(handler())
client.loop.create_task(main())
#client.run_until_disconnected()
#client.loop.run_until_complete(main())
client.run_until_disconnected()