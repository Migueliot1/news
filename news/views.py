import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Article, Searchables
from users.models import Profile, Comment, Answer, Activity
from users.forms import AnswerForm

import urllib.request, urllib.parse, urllib.error

from scheduler.utils import download_image

# Create your views here.


def showNews(request):
    articles = Article.objects.all().order_by('-raw_publish_time')

    for article in articles:
        if article.image_path == 'imgs/article_default.png':
            # Download image if it's not downloaded
            img_path = download_image(
                article.image_link_id.link + article.image_link_main, 
                article.image_link_main)
            article.image_path = img_path

    context = {'articles': articles}

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context = {'articles': articles, 'profile': profile}

    return render(request, 'news/show_news.html', context)


def showArticle(request, pk):


    answer_form = AnswerForm()
    context = {'answer_form': answer_form, 'answer':'', 'comment':'', 
                'activity':'', 'activity_type':''}
    
    article = Article.objects.get(link_main=pk)
    comments = article.comment_set.all()
    answers = Answer.objects.all()
    context['article'] = article
    context['comments'] = comments
    context['answers'] = answers


    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['profile'] = profile

        if request.method == 'POST':

            if request.POST.get('comment'):
                Comment.objects.create(
                    owner=profile, post=article, comment_body=request.POST.get('comment'))
            
            elif request.POST.get('answered_comment_id'):
                print(request.POST)
                # Add to utils as function 'saveAnswer'
                form = AnswerForm(request.POST)
                answer = form.save(commit=False)
                answer.answer_to = Comment.objects.get(id=request.POST.get('answered_comment_id'))
                answer.owner = profile
                answer.post = article
                answer.is_answer = True
                answer.save()

            elif request.POST.get('upvoted_comment_id'):
                
                comment_id = request.POST.get('upvoted_comment_id')
                comment = Comment.objects.get(id=comment_id)

                # Check if there's downvote from the user to the comment
                # If there is => delete it and create upvote
                try:
                    downvote = Activity.objects.get(user=profile, activity_type='D', 
                                to_comment=comment)
                    downvote.delete()
                    Activity.objects.create(user=profile, activity_type='U', 
                                to_comment=comment)
                except:
                    # Check if the comment was already upvoted
                    try:
                        upvote = Activity.objects.get(user=profile, activity_type='U', 
                                to_comment=comment)
                        # Remove upvote if no exception caught
                        upvote.delete()
                    except:
                        Activity.objects.create(user=profile, activity_type='U', 
                                to_comment=comment)

            elif request.POST.get('downvoted_comment_id'):
  
                comment_id = request.POST.get('downvoted_comment_id')
                comment = Comment.objects.get(id=comment_id)
                
                # Check if there's upvote from the user to the comment
                # If there is => delete it and create downvote
                try:
                    upvote = Activity.objects.get(user=profile, activity_type='U', 
                            to_comment=comment)
                    upvote.delete()
                    Activity.objects.create(user=profile, activity_type='D', 
                                to_comment=comment)
                except:
                    # Check if the comment was already downvoted
                    try:
                        downvote = Activity.objects.get(user=profile, activity_type='D', 
                                to_comment=comment)
                        # Remove downvote if no exception caught
                        downvote.delete()
                    except:
                        # Create new downvote in the DB
                        Activity.objects.create(user=profile, activity_type='D', 
                                to_comment=comment)


    return render(request, 'news/article.html', context)


def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    article_link = comment.post.link_main
    comment.delete()

    return redirect('single_article', pk=article_link)

def aboutPage(request):

    print('yes')
    context = {}

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['profile'] = profile

    return render(request, 'news/about.html', context)
