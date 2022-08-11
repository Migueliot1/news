from django.db import models
import uuid

# Create your models here.

class ImageWebsite(models.Model):
    '''
    The website from which the article image will be downloaded.

    Consists of website's name, link and number of / after which link should be saved.

    E.g.: if the URL is https://www.website.com/image.png then the results after chopping on / will be:
    chop[0] = 'https:'\n
    chop[1] = ''\n
    chop[2] = 'www.website.com'\n
    chop[3] = 'image.png'
    
    Because the needed result is chop[3] then num_to_chop should be 3.
    '''

    website_name = models.CharField(max_length=200)
    link = models.CharField(max_length=2000)
    num_to_chop = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)

    def __str__(self):
        return str(self.website_name)


class NewsWebsite(models.Model):
    '''
    The website from which the article data will be saved.
    
    Consists of website's name, main link with various articles, foreign key of link to download article image from, and link for specific article.
    '''

    website_name = models.CharField(max_length=200)
    get_news_link = models.CharField(max_length=2000)
    get_image_link = models.ForeignKey(
                    ImageWebsite, on_delete=models.SET_NULL, null=True, blank=True)
    link = models.CharField(max_length=2000)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)

    def __str__(self):
        return str(self.website_name)


class Article(models.Model):
    '''
    The model for each article.

    Consists of title, synopsis (if exists), foreign key for the website, 
    link part after last /, foreign key of image download website, 
    image link part after last /, image path on the sever (added automaticly), 
    publish time (added automaticl; ready for showing), raw publish time, 
    and a boolean if the website was published or not.
    '''

    title = models.CharField(max_length=500)
    synopsis = models.CharField(max_length=2000, null=True, blank=True)
    link_id = models.ForeignKey(
            NewsWebsite, on_delete=models.SET_NULL, null=True, blank=True)
    link_main = models.CharField(max_length=2000, unique=True)
    image_link_id = models.ForeignKey(
            ImageWebsite, on_delete=models.SET_NULL, null=True, blank=True)
    image_link_main = models.CharField(max_length=2000, null=True, blank=True)
    image_path = models.CharField(max_length=2000, null=True, blank=True, default='imgs/article_default.png')
    publish_time = models.CharField(max_length = 200, null=True, blank=True)
    raw_publish_time = models.CharField(max_length=200, null=True, blank=True)
    was_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=True)

    def __str__(self):
        return str(self.title)


class Searchables(models.Model):
    '''
    The model of variables for re library to find needed data 
    for each stored article.

    Consists of searchables to find the whole article, then article's title, 
    link, synopsis, link to download image from, and publish time.

    (NOT FINAL; WILL BE REPLACED TO JSON SEARCHABLES)
    '''

    website = models.ForeignKey(NewsWebsite, on_delete=models.CASCADE, null=True, blank=True)
    article = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    article_link = models.CharField(max_length=500, null=True, blank=True)
    synopsis = models.CharField(max_length=500, null=True, blank=True)
    image_link = models.CharField(max_length=500, null=True, blank=True)
    time = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.website)
