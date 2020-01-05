import socks
import logging
from telethon.sync import TelegramClient, events

import time
import argparse
import json
import sys
import os
import time

logging.basicConfig(level=logging.INFO,
	format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
	datefmt="%d-%m-%Y %H:%M:%S",
	stream=sys.stdout)

parser = argparse.ArgumentParser(description='Script create session file')

parser.add_argument(
	'-f',
	'--file',
	type = str,
	dest='file',
	help = 'Input JSON file of accaunts',
	default='accaunts.json')

parser.add_argument(
	'-n',
	'--number',
	type = int,
	dest='number',
	help = 'Accaunt number',
	default=0)

parser.add_argument(
	'-t',
	'--tor',
	action='store_const',
	const=True)

args = parser.parse_args()

with open(args.file, 'r') as f:
    data = json.loads(f.read())

#print(args.file)
#print(args.number)

if len(data['accaunts']) <= args.number:
	logging.info('The index went beyond')
	#print("The index went beyond")
	sys.exit(-1)

i = 0
for accaunt in data["accaunts"]:
	if i == args.number:
		break;
	i += 1

if args.tor:
	logging.info("Starting TOR")
	#print("Starting TOR")
	os.system("/bin/tor SOCKSPort %s ExitRelay 0 ExcludeExitNodes {ru},{ua},{by},{kz},{??} StrictNodes 1" % int(9051 + args.number))

client = TelegramClient("sessions\%s.session" % accaunt["title"], int(accaunt["api_id"]), accaunt["api_hash"], proxy=(socks.SOCKS5, "127.0.0.1", int(9051 + args.number)))

client.start()

#while True:
#	logging.info("Something from %s process" % argv[1])
#	time.sleep(5)

me = client.get_me()

print(me.username, flush=True)
print(me.phone, flush=True)

litecoin = client.get_entity("Litecoin_click_bot")
print(litecoin.id)
print(litecoin)
