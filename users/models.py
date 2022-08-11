from django.db import models
from django.contrib.auth.models import User

from news.models import Article

import uuid

# Create your models here.

class Profile(models.Model):
    '''
    Main profile model.

    Consist of Django user saved in the database, email, username, 
    short bio (optional), and profile image (optional).
    '''

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    short_bio = models.CharField(max_length=1000, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, 
                                    upload_to='static/imgs/profiles/', default='static/imgs/profiles/profile_default.png')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                        primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)


class Comment(models.Model):
    '''
    Model for each saved comment.

    Consists of commentator's profile, comment's post, body, 
    foreign keys to its answers, boolean to if this comment 
    is an answer to other comment, and foreign keys to upvotes 
    and downvotes to this comment.
    '''

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    comment_body = models.TextField(max_length=2000)
    answers = models.ManyToManyField('Answer', blank=True)
    is_answer = models.BooleanField(default=False)
    activities = models.ManyToManyField('Activity', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                        primary_key=True, editable=False)

    def __str__(self):
        return str(self.comment_body)


class Answer(Comment):
    '''Model for answer.
    
    Since it's a child object from Comment it has same parameters 
    but also a foreign key for a comment which the current comment 
    answers to.
    '''

    answer_to = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, related_name='answer_to_comment')


class Activity(models.Model):
    '''
    Model for activities such as upvotes and downvotes.

    Consists of user's profile who left the comment, type of activity - 
    upvote or downvote, and foreign key of voted comment.
    '''

    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = ( 
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    to_comment = models.ForeignKey(Comment, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.activity_type)


class Message(models.Model):
    '''
    Model for every sended message.

    Consists of sender's profile, recipient's profile, message's subject, 
    body, and boolean if the message was read or not.
    '''

    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                        primary_key=True, editable=False)

    def __str__(self):
        return self.subject 

    class Meta:
        ordering = ['is_read', '-created']