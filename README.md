# ScrapeGram

##  Scraping data from Instagram

This project allows you to collect someone's account data from Instagram. Here a bunch of data that you can collect with this tool :

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

## How to install ScrapeGram ?

Clone the repo :
```bash
git clone git@github.com:pierreleocadie/ScrapeGram.git
```
Then install requirements :
```bash
pip install -r requirements.txt
```

## Setup  ScrapeGram

In the ```src/``` folder open the ```settings.json``` file. Provide your username and password to allow ScrapeGram to log into your Instagram account, and then provide the username of the target you want to collect data on.

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
python main.py
```
or 
```bash
python3 main.py
```