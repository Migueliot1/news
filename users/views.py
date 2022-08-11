import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import Profile, Comment, Message
from django.contrib.auth.decorators import login_required


# Create your views here.

def loginPage(request):
    '''Render login/register page.'''

    # If user is already logged in then redirect to the main page
    if request.user.is_authenticated:
        return redirect('news_main')

    if request.method == 'POST':

        # Check for register form
        if request.POST.get('password2', False):
            print(request.POST)
            registerForm = SignUpForm(request.POST)
            if registerForm.is_valid():
                newUser = registerForm.save(commit=False)
                newUser.username = newUser.username.lower()
                newUser.save()
        # Check for login form
        elif request.POST.get('Username_login', False):
            print(request.POST)
            username = request.POST['Username_login']
            password = request.POST['Password_login']

            # Check if username and password are correct
            try:
                user = User.objects.get(username=username)
            except:
                # Show flash message if profile with this username doesn't exist
                print('Username does not exist') # WILL BE A FLASH MESSAGE

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                # Show flash message that username/password incorrect
                print('Username or password is incorrect') # WILL BE A FLASH MESSAGE
    
    registerForm = SignUpForm()

    context = {'registerForm': registerForm}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    '''Logout user when button pressed.'''

    logout(request)
    return redirect('news_main')


def userProfile(request, pk):
    '''Render user's profile.'''

    context = {}

    # Get profile with id 
    single_user = Profile.objects.get(id=pk)
    comments = Comment.objects.filter(owner=single_user).order_by('-created')

    # For menu on the right if user is logged in
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)


    context = {'single_user': single_user, 'comments': comments, 'profile': profile}
    return render(request, 'users/user_profile.html', context)


@login_required(login_url='login')
def inbox(request):
    '''Render user's personal inbox.'''

    context = {}

    # For menu on the right if user is logged in
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

    # Get all messages and a number of undread messages
    inboxMessages = profile.messages.all()
    unreadCount = inboxMessages.filter(is_read=False).count()
    context = {'profile': profile, 'inboxMessages': inboxMessages, 
                'unreadCount': unreadCount}

    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    '''Render each sent message.'''
    
    profile = Profile.objects.get(user=request.user)
    message = Message.objects.get(id=pk)

    # Change read's message from False to True
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'profile': profile, 'message': message}

    return render(request, 'users/message.html', context)


@login_required(login_url='login')
def createMessage(request, pk):
    '''Render page for sending a message.'''

    # Get profile of user and profile of recipient
    profile = Profile.objects.get(user=request.user)
    recipient = Profile.objects.get(id=pk)

    # Redirect to recipient's profile if user wants to send
    # message to themselves
    if profile == recipient:
        return redirect('user_profile', pk)

    context = {'profile': profile, 'recipient': recipient, 'subject': '', 'body': ''}
    
    # If user pressed 'Send message'
    if request.method == 'POST':
        # Check if message's subject and body are ok
        if request.POST.get('subject', False) and request.POST.get('body', False):
            Message.objects.create(sender=profile, recipient=recipient, subject=request.POST.get('subject'),
                    body=request.POST.get('body'))
        else:
            # Show a flash message if there was smth wrong with the sent message
            print(request.POST) # FOR DEBUG; WILL BE A FLASH MESSAGE

    return render(request, 'users/message_form.html', context)
