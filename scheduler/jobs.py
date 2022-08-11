import re
from datetime import datetime, timedelta
from dateutil import parser

from news.models import Searchables, Article
from .utils import get_searchables, download_data, download_image, prepare_string

# Temporary txt to store data in
temp_path = 'static/files/temp_data.txt'


def prepare_time(raw_time):
    '''Prepare time to be stored in database.'''
    
    # If website is Kotaku (it has a weird name)
    if "-04:00" in raw_time:
        date = datetime.fromisoformat(raw_time)
        date += timedelta(hours=4)

    else: # If any other website
        date = parser.parse(raw_time)

    raw_result_str = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    result = date.strftime('%d %b %Y | %H:%M UTC')
    
    return (result, raw_result_str)


def find_contents(searchables):
    '''Finding in HTML file articles' contents and saving them 
    to database.
    
    Gets searchables terms as a tuple to extract way to find each article, name, link, etc.
    Searchables tuple should be (article, name, link, synopsis, image, time)'''

    # Getting raw HTML contents from the saved temp file
    file = open(temp_path, 'r')
    data = file.read()
    file.close()

    # Browsing through articles
    # Condition allows correct work on Kotaku website
    if 'div' in searchables.article:
        arts_list = re.findall(searchables.article, data, re.DOTALL)
    else:
        arts_list = re.findall(searchables.article, data)

    articles_data = list()
    
    # Extracting PC Gamer news articles
    for item in arts_list:

        # Checking if it's news or deals article on PC Gamer and skipping if it's not news
        check = re.search('<a class="category-link" href="javascript:void.+?">(.+?)</a>', item)
        # if check is None:
        #     print('check: none')
        if check:
            check_category = check.group(1).lower()
            # DEBUG
            # print('check:', check_category)
            if 'ews' not in check_category:
                continue
        

        # Searching for articles' link
        ml = re.search(searchables.article_link, item)
        if ml:
            # for some reason link to the next page is also added to the list so I have to do this workaround
            link = ml.group(1)
            if link == 'https://www.pcgamer.com/news/page/2/':
                link = None

            # Check if it's something else on PC Gamer
            if 'pcgamer' in link and (check is None or 'ews' not in check_category):
                # print(link)
                link = None
                continue
        else:
            link = None
        
        # Searching for article's title
        mn = re.search(searchables.title, item)
        if mn:
            title = mn.group(1)
        else:
            title = None


        # Searching for synopsis
        ms = re.search(searchables.synopsis, item, re.DOTALL)
        if ms:
            synopsis = ms.group(1)
        else:
            synopsis = None

        # Searching for image's link
        mi = re.search(searchables.image_link, item)
        if mi:
            img_link = mi.group(1)
            # Skipping top "NEWS" image
            if 'd5f041deff81d2edcceffde2dbbb7981' in img_link:
                img_link_search = re.findall(searchables.image_link, item)
                img_link = img_link_search[1]
                
            if 'data-chomp-id' in searchables.image_link:
                img_link = img_link.replace('" data-format="', '.')
                #print('img:', img_link)
        else:
            img_link = None

        # Searching for time
        mt = re.search(searchables.time, item)
        if mt:
            time = mt.group(1)
        else:
            time = None

        # DEBUG
        # print('title:', title, 'link:', link, 'synopsis:', synopsis, 'img_link:', img_link, 'time:', time)

        if title and link and synopsis and img_link and time:
            
            # Append tuple with all of the data inside this list
            articles_data.append(
                (title, 
                synopsis, 
                link, 
                img_link, 
                time, 
                searchables.website, 
                searchables.website.get_image_link,
                searchables.website.get_image_link.num_to_chop)
            )
        else:
            print('check fault')


    return articles_data


def save_arts(articles_data):
    '''Saves clean articles' data into the database 
    and returns number of added articles.'''


    # Add a newly gotten article to the database
    length = len(articles_data)
    new_arts_count = 0
    old_arts_count = 0

    # Check if there is any data at all
    if length > 0:
        for i in range(length):

            # Fill local variables with given data
            title = prepare_string(articles_data[i][0])
            synopsis = prepare_string(articles_data[i][1])
            article_link = articles_data[i][2]
            full_img_link = articles_data[i][3]
            raw_time = articles_data[i][4]
            website = articles_data[i][5]
            img_website = articles_data[i][6]
            img_num_to_chop = articles_data[i][7]

            if title is None or synopsis is None or article_link is None or full_img_link is None or raw_time is None or website is None or img_website is None:
                continue
            
            # Preparing links to be stored
            # First, article's link
            article_link = article_link.split('/')[3] # Getting link piece after '.com/'
            
            # Second, image's link 
            img_link = full_img_link.split('/')[img_num_to_chop]
            if img_num_to_chop == 0:
                img_link = full_img_link
                full_img_link = 'https://i.kinja-img.com/gawker-media/image/upload/c_fill,f_auto,g_center,h_900,pg_1,q_60,w_1600/' + img_link

            # Third, download image and save its filepath
            img_path = download_image(full_img_link, img_link)

            # Fourth, prepare time
            time_tuple = prepare_time(raw_time)

            # If everything is good then create Article instance in the database
            try:
                obj = Article.objects.create(
                    title=title, 
                    synopsis=synopsis, 
                    link_id=website, 
                    link_main=article_link, 
                    image_link_id=img_website, 
                    image_link_main=img_link, 
                    image_path=img_path, 
                    publish_time=time_tuple[0],
                    raw_publish_time=time_tuple[1]
                )
                new_arts_count += 1
            except:
                old_arts_count += 1

        print('Downloaded and stored', new_arts_count, 'articles, and ignored', old_arts_count, 'articles.')
        