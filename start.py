import argparse
import json
import os

parser = argparse.ArgumentParser(description="Script added id field in JSON file")

parser.add_argument(
	"-if",
	"--input-file",
	type = str,
	dest="inputFile",
	help = "Input JSON file of accaunts",
	default="accaunts.json")

parser.add_argument(
	"-of",
	"--output-file",
	type = str,
	dest="outputFile",
	help = "Output supervisor file",
	default="/etc/supervisor/conf.d/worker.conf")

parser.add_argument(
	"-ocf",
	"--output-count-file",
	type = str,
	dest="outputCountFile",
	help = "Output supervisor file",
	default="count")

args = parser.parse_args()

with open(args.inputFile, "r") as inputFile:
    data = json.loads(inputFile.read())

#print(len(data["accaunts"]))
count = len(data["accaunts"])

with open(args.outputFile, "w+") as outputFile:
	outputFile.write('''[program:workers]
process_name=%(program_name)s_%(process_num)1d
command=/bin/python3 /home/user/workers/worker.py %(process_num)s
stdout_logfile=/home/user/workers/log/worker%(process_num)1d.log
stderr_logfile=/home/user/workers/log/worker_stderr_%(process_num)1d.log
autostart=true
user=root
stopsignal=KILL\n''')
	outputFile.write("numprocs=%s" % count)

	if not os.path.exists("log"):
		print("Create log directory")
		os.mkdir("log")
	else:
		if os.path.isfile("log"):
			print("log is file")
		

with open(args.outputCountFile, "w+") as outputCountFile:
	outputCountFile.write("%s\n" % count)

for number in range(count):
	print("Starting TOR on port %s" % int(9051 + number))
	os.system("/bin/tor --allow-missing-torrc SOCKSPort %s DataDirectory /var/lib/tor%s ExitRelay 0 ExcludeExitNodes {ru},{ua},{by},{kz},{??} StrictNodes 1 &" % (int(9051 + number), number))


