from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from first_app.forms import UserForm, ProfileForm

# Create your views here.
from first_app.models import AccessRecord, UserProfileInfo
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'first_app/index.html', {})


@login_required()
def web_records(request):
    webpages = AccessRecord.objects.select_related('name').order_by('date')
    data = {'data': webpages}
    return render(request, 'first_app/web_records.html', context=data)


def help_page(request):
    return render(request, 'first_app/help_page.html')


def users(request):
    dbuser = UserProfileInfo.objects.order_by('pk')
    userdata = {'users': dbuser}
    return render(request, 'first_app/users.html', context=userdata)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'first_app/register.html',
                  {'form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return web_records(request)
            else:
                return HttpResponse('Account not active')

        else:
            print('Someone try to login and failed!')
            print('Username: {} and password: {}'.format(username, password))
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'first_app/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return index(request)
