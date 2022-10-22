![logo](https://cdn.discordapp.com/attachments/764495556801331211/1005884280796368906/Logo-white.png)
# ScrapeGram

##  Scraping data from Instagram

This project allows you to collect data from someone's Instagram account. Here a bunch of data that you can collect with this tool :

- Currently available :
    * Followers list 
    * Following list

- Incoming :
    * Posts (Photos, Videos)
    * Comments
    * Tagged posts
    * Stories
    * Geolocation

I've more ideas for features, I'll update this README file to make it clear at the right time.

## Before install

**DISCLAIMER : ScrapeGram IS FOR EDUCATIONAL PURPOSE ONLY. By using ScrapeGram, you are violating the Instagram community rules, so do not use your personal Instagram account with ScrapeGram or you will be banned. Use ScrapeGram at your own risk.***

## How to install ScrapeGram ?

**You must be using Python version ```3.10.0``` or later.**

Clone the repo :
```bash
git clone git@github.com:pierreleocadie/ScrapeGram.git
```
Then install requirements :
```bash
pip install -r requirements.txt
```

## Setup  ScrapeGram

In the ```src/``` folder open the ```settings.json``` file. Provide your username and password to allow ScrapeGram to log into your Instagram account. Then provide the username of the target you want to collect data on.

```json
"username_account": "your_username",
"password_account": "your_password",
"username_target_account" : "username_of_the_target"
```

You can also change the parameters of the queries. You can change: - the minimum and maximum delay you want between each request - the number of edges you want to get (edge = group of followers or following) - the number of followers or following you want to get per edge.

```json
"queries_parameters": {
 "min_delay_between_request": 10,
 "max_delay_between_request": 20,
 "max_number_of_edges_to_get": 1,
 "number_of_followers_following_to_get_per_edge": 10
}
```

Run ScrapeGram in the ```main.py``` file or with these commands :
```bash
cd ScrapeGram
python src/main.py
```
or 
```bash
cd ScrapeGram
python3 src/main.py
```
or
```bash
cd ScrapeGram
python src/main.py -u [your_username] -p [your_password] -t [username_of_the_target]
```
or
```bash
cd ScrapeGram
python3 src/main.py -u [your_username] -p [your_password] -t [username_of_the_target]
```
