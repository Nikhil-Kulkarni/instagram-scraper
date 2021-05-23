from datetime import datetime
from modules import compare
from modules import file_io
from modules import stats
from random import random
from random import randint
import time
import psycopg2

from modules.scraper import Scraper
from modules.profiler import Profiler
from modules.utils import ask_input, ask_multiple_option


groups = ['followers', 'following']

# Ask for input
target = ask_input('Enter the target username: ')
group = ask_multiple_option(options = groups + ['both']);
option = ask_input('0) profile downloader 1) following scraper: ')
usernames = []
passwords = []

def scrape(group, option):
    differs = False
    startTime = datetime.now()
    userIndex = 0

    if option == 1:
        scraper = Scraper()
        scraper.authenticate(usernames[userIndex], passwords[userIndex])
        users = scraper.get_users(group, target, None, verbose=True)
        for index, user in enumerate(users):
            new_users = scraper.get_users(group, None, user, verbose=True)
            if new_users is None or index % randint(20, 42) == 0:
                userIndex = (userIndex + 1) % 3
                scraper.close()
                scraper = Scraper()
                scraper.authenticate(usernames[userIndex], passwords[userIndex])
            else:
                users.extend(new_users)

        scraper.close()

        last_users = file_io.read_last(target, group)
        if last_users:
            differs = bool(compare.get_diffs(users, last_users))

        if (differs or not last_users):
            file_io.store(target, group, users)
        # Stats
        stats.numbers(len(users), scraper.expected_number)
        if (differs): stats.diff(users, last_users)
        print('Took ' + str(datetime.now() - startTime))
    else:
        print('connecting to Postgres')
        conn = psycopg2.connect(
            host="localhost",
            database="creators_store",
            user="postgres",
            password="postgres")
        f = open('everything.txt', 'r');
        lines = f.readlines()
        profiler = Profiler()
        profiler.authenticate(usernames[userIndex], passwords[userIndex])
        iteration = 1

        sql = """
        INSERT INTO creators(id, username, biography, external_url, full_name, is_business_account, is_professional_account, business_email, business_phone_number, business_category_name, category_name, followers_count, following_count, is_private)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
        """

        for link in lines:
            if iteration % randint(50, 75) == 0:
                userIndex = (userIndex + 1) % 2
                profiler.close()
                profiler = Profiler()
                profiler.authenticate(usernames[userIndex], passwords[userIndex])
            username = link.split('https://www.instagram.com/', 1)[1].split('/')[0]
            profile = profiler.get_user_profile(username)
            user = profile['graphql']['user']
            if not user['is_private']:
                followers_count = user['edge_followed_by']['count']
                following_count = user['edge_follow']['count']
                cur = conn.cursor()
                cur.execute(sql, (user['id'], user['username'], user['biography'], user['external_url'], user['full_name'], user['is_business_account'], user['is_professional_account'], user['business_email'], user['business_phone_number'], user['business_category_name'], user['category_name'], followers_count, following_count, user['is_private']))
                conn.commit()
                cur.close()
            iteration = iteration + 1
            time.sleep(random() * randint(1, 5))
        conn.close()
        profiler.close()

if (group == 'both'):
    for group in groups:
        scrape(group, option)
else:
    scrape(group, option)
