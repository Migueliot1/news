from django import template
import markdown
from django.utils.safestring import mark_safe

from users.models import Profile, Comment, Activity
from ..models import Article


register = template.Library()


@register.filter(name='comment_rating')
def comment_rating(comment_id):
    '''Return the overall rating of the comment.'''

    comment = Comment.objects.get(id=comment_id)
    activities = comment.activity_set.all()
    upvotes = activities.filter(activity_type='U').count()
    downvotes = activities.filter(activity_type='D').count()

    rating = upvotes - downvotes

    return rating


@register.filter(name='upvote_check', takes_context=True)
def upvote_check(comment_id, profile_id):
    '''Returns true if an upvote exists, otherwise returns false.'''

    profile = Profile.objects.get(id=profile_id)
    comment = Comment.objects.get(id=comment_id)
    try:
        upvote = Activity.objects.get(user=profile, activity_type='U', to_comment=comment)
        return True
    except:
        return False


@register.filter(name='article_comments_count')
def article_comments_count(article_id):
    '''Return an amount of comments the article has.'''

    article = Article.objects.get(id=article_id)
    comments_num = Comment.objects.filter(post=article).count()
    
    return comments_num


@register.filter(name='downvote_check', takes_context=True)
def downvote_check(comment_id, profile_id):
    '''Returns true if the downvote exists, otherwise returns false.'''

    # Get comment and do the check with try/except
    profile = Profile.objects.get(id=profile_id)
    comment = Comment.objects.get(id=comment_id)
    try:
        downvote = Activity.objects.get(user=profile, activity_type='D', to_comment=comment)
        return True
    except:
        return False

@register.filter(name='rating_count')
def rating_count(user_id):
    '''Returns rating of all user's comments combined.'''

    # Get all comments from the selected user
    user_profile = Profile.objects.get(id=user_id)
    comments = Comment.objects.filter(owner=user_profile)

    # Counting rating of all comments left by the user combined
    count = 0
    for comment in comments:
        count += comment_rating(comment.id)

    return count
    