import time
from sys import argv
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    stream=sys.stdout)

while True:
	logging.info('Something from %s process' % argv[1])
	time.sleep(5)
