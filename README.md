# DOGEWorker

[![Social](https://img.shields.io/badge/social-telegram-lightgray.svg)](https://teleg.run/c1ewd)
[![Donations](https://img.shields.io/badge/donations-Liberapay-green.svg)](https://liberapay.com/c1ewd/donate)

Sources of coinworker which works with DOGE click 

## List of package

- PySocks==1.7.1
- selenium==3.141.0
- Telethon==1.10.10
- utllib3==1.25.7

## Activate virtualenv

```
source venv/bin/activate
```

## Prepare first start

```
sudo python3 start.py
```

Creating start config for `supervisor` and starting `tor` for N ports
 
## Start selenium

```
sudo java -jar selenium-server-standalone-3.141.59.jar
```

## Start worker

```
sudo python3 worker -n 1
```

## Format accaunts.json

```
{ 
	"accaunts": [
			{
				"id": X,
				"phone": "+XXXXXXXXXXX",
				"title": "XXXXXXXX",
				"api_id": "XXXXXXX",
				"api_hash": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
			},
			...

		]
}
```

## Donations (Optional)

[![Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/c1ewd/donate)
