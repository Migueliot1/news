import urllib.request, urllib.parse, urllib.error
import ssl

from news.models import Searchables


temp_path = 'static/files/temp_data.txt'


def prepare_string(string):
    '''Delete all the custom text styling used in news website.'''

    string = string.replace("&ndash;", "-")
    string = string.replace("&mdash;", "-")
    string = string.replace("&amp;", "&")
    string = string.replace("<i>", "")
    string = string.replace("</i>", "")
    string = string.replace("<em>", "")
    string = string.replace("</em>", "")
    string = string.replace("&#x27;", "'")
    string = string.replace("<!-- -->", "")

    return string


def get_searchables():
    '''Get searchables from the database in a format of tuple 
    (article, name, link, synopsis, image, time).
    '''

    # List of searchables for each website
    all_searchables = Searchables.objects.all()

    return all_searchables


def download_data(url):
    '''Getting published articles from the given website'''

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urllib.request.urlopen(url, context=ctx) # Save page contents
    data = html.read().decode() # Decode contents
    print('Retrieved', len(data), 'characters from URL', url)

    # Save html contents to a temp file
    file = open(temp_path, 'r+')
    file.truncate(0)
    data = data.replace("\u017b", "")
    data = data.replace("\u0142", "")
    file.write(data)
    file.close()


def download_image(website_url, img_url):
    '''Downloads image from given URL and returns its filepath.'''

    url = website_url
    filepath = 'static/imgs/' + img_url
    urllib.request.urlretrieve(url, filepath)

    return 'imgs/' + img_url
