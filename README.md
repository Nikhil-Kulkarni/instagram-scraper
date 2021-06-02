# Instagram scraper
This tool helps you scrape users following graph and all their publicly available metadata. In main.py, add your username/password to usernames and passwords arrays. The script rotates credentials at random intervals to attempt to get around Instagram's spam detection. I highly recommend having 8-10 credential pairs you can rotate through.

## Scraping Options
Option 0 scrapes individual profiles for all their metadata. It reads a list of profile links from links.txt. See an example of what data you can gather: https://www.instagram.com/kyliejenner/?__a=1
Option 1 scrapes following graphs. Seed the script with an initial username and it'll output links of the following graph for your seed, who their following, etc. until you stop the script. You can use option 1 to seed option 0.

## Setup
Active virtual env via: `source venv/bin/activate`
Install dependencies: `pip install -r requirements.txt`

For option 0, setup a local postgres instance to store the outputted metadata. Create a creators_store table as follows:

`create table creators(
	id bigint not null primary key,
	username varchar,
	biography varchar,
	external_url varchar,
	full_name varchar,
	is_business_account boolean,
	is_professional_account boolean,
	business_email varchar,
	business_phone_number varchar,
	business_category_name varchar,
	category_name varchar,
	followers_count integer,
	following_count integer,
	is_private boolean
);`

Enter your db credentials in main.py. You can query really easily with basic sql for creator categories, emails, followers_count, etc. 
Option 1 writes profile links to a local txt file.

Run the script via: `python main.py`  

## Disclaimer
WARNING: DO NOT USE YOUR PERSONAL IG ACCOUNT. AFTER SEVERAL HUNDRED THOUSAND REQUESTS, IG WILL TEMPORARILY LOCK YOU OUT. I RECOMMEND MAKING 8-10 FAKE ACCOUNTS YOU CAN ROTATE.
