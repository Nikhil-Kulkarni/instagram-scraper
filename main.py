from datetime import datetime
from modules import compare
from modules import file_io
from modules import stats

from modules.scraper import Scraper
from modules.utils import ask_input, ask_multiple_option


groups = ['followers', 'following']

# Ask for input
target = ask_input('Enter the target username: ')
group = ask_multiple_option(options = groups + ['both']);
usernames = ['', '', '', '', '', '', '', '', '', '', '', '', '', '']
passwords = ['', '', '', '', '', '', '', '', '', '', '', '', '', '']

def scrape(group, user):
    differs = False
    scraper = Scraper()
    startTime = datetime.now()
    userIndex = 0
    
    scraper.authenticate(usernames2[userIndex], passwords2[userIndex])

    users = scraper.get_users(group, target, None, verbose=True)
    for index, user in enumerate(users):
        new_users = scraper.get_users(group, None, user, verbose=True)
        if new_users is None or index % 7 == 0:
            userIndex = (userIndex + 1) % 1
            scraper.close()
            scraper = Scraper()
            scraper.authenticate(usernames2[userIndex], passwords2[userIndex])
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

if (group == 'both'):
    for group in groups:
        scrape(group, user)
else:
    scrape(group, user)
