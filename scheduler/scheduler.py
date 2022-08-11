from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from .jobs import get_searchables, download_data, find_contents, save_arts

from datetime import datetime

# # This is the function you want to schedule - add as many as you want and then register them in the start() function below
def test_msg():
    print('testing')
    

def check_news():
    '''Function used to download news from various websites.'''

    # Get current time
    now = datetime.now()

    # Translate time to format dd/mm/YY H:M:S and print time of check
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print('Regular check', dt_string)

    # Get searchables
    all_searchables = get_searchables()
    
    # For each website do a check if there any new articles
    for searchable in all_searchables:

        download_data(searchable.website.get_news_link) # Download data from the website
        articles_data = find_contents(searchable) # Find articles' contents such as title, image link, synopsis, etc.
        save_arts(articles_data) # Save new articles in the database


def start():
    '''Main function to start scheduler.'''

    scheduler = BackgroundScheduler()

    scheduler.add_job(check_news, 'interval', minutes=15, id='get_news')
    scheduler.start()
