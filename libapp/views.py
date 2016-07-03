import datetime
import random
from libapp.util import util
from libapp.models import User
from django.shortcuts import render
from libapp.models import LibItem, LibUser, Dvd, Book, Suggestion
from django.shortcuts import get_list_or_404
from libapp.forms import SuggestionForm, SearchLibForm, LoginForm, RegisterForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def search_lib(request):
    result = check_login(request)
    if result is not None:
        return result
    if request.method == 'POST':
        form = SearchLibForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            name = form.cleaned_data['name']
            results = []
            result1 = Book.objects.filter(Q(title__icontains=title), Q(author__icontains=name))
            result2 = Dvd.objects.filter(Q(title__icontains=title), Q(maker__icontains=name))
            results.extend(result1)
            results.extend(result2)
            return render(request, 'libapp/SearchLib.html', {'form': form, 'results': results})
    else:
        form = SearchLibForm()
    return render(request, 'libapp/SearchLib.html', {'form': form})


def suggestions(request):
    result = check_login(request)
    if result is not None:
        return result
    suggestion_list = Suggestion.objects.all()
    return render(request, 'libapp/Suggestions.html', {'suggestion_list': suggestion_list})


def new_item(request):
    result = check_login(request)
    if result is not None:
        return result
    suggestion_list2 = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('libapp:suggestions'))
        else:
            return render(request, 'libapp/NewItem.html', {'form': form, 'suggestion_list2': suggestion_list2})
    else:
        form = SuggestionForm()
        return render(request, 'libapp/NewItem.html', {'form': form, 'suggestion_list2': suggestion_list2})


def details(request, item_id):
    result = check_login(request)
    if result is not None:
        return result
    items = get_list_or_404(LibItem, id=item_id)
    for item in items:
        if item.itemtype == 'Book':
            result = get_list_or_404(Book, id=item_id)
        else:
            result = get_list_or_404(Dvd, id=item_id)
    return render(request, 'libapp/Details.html', {'result': result})


def index(request):

    if 'lucky_num' in request.session:
        session_msg = request.session['lucky_num']
    else:
        session_msg = 0

    response = render(request, 'libapp/Index.html', {'session_msg': session_msg})

    if 'about_visits' in request.COOKIES:
        about_visits = int(request.COOKIES['about_visits'])
        response.set_cookie('about_visits', about_visits + 1, max_age=300)
    else:
        response.set_cookie('about_visits', 1, max_age=300)
    return response


def books(request):
    result = check_login(request)
    if result is not None:
        return result
    book_list = Book.objects.all().order_by("-pub_year")[:10]
    return render(request, 'libapp/Books.html', {'book_list': book_list})


def dvds(request):
    if not request.user.is_authenticated():
        return render(request, 'libapp/Index.html', {'log_msg': 'Please login first.'})
    dvd_list = Dvd.objects.all().order_by("-pub_year")[:10]
    return render(request, 'libapp/Dvds.html', {'dvd_list': dvd_list})


def others(request):
    result = check_login(request)
    if result is not None:
        return result
    other_list = ["Other_" + str(x) for x in range(1, 20)]
    return render(request, 'libapp/Others.html', {'other_list': other_list})


def my_item(request):
    result = check_login(request)
    if result is not None:
        return result
    if len(LibUser.objects.all().filter(id=request.user.id)) > 0:
        item_list = LibItem.objects.all().filter(checked_out=True).filter(user=request.user.id)
        if len(item_list) == 0:
            return render(request, 'libapp/MyItem.html', {'error_msg': "No item is checked out by you!"})
        else:
            return render(request, 'libapp/MyItem.html', {'item_list': item_list})
    else:
        return render(request, 'libapp/MyItem.html', {'error_msg': "You are not a Library User!"})


def my_acct(request):
    result = check_login(request)
    if result is not None:
        return result
    msg = "Hello User!"
    return render(request, 'libapp/MyAcct.html', {'msg': msg})


def base(request):
    return render(request, 'libapp/MainBase.html')


def about(request):
    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    opt_time = dict.fromkeys(["Monday", "Tuesday", "Wednesday", "Thursday"], [8.30, 12, 13.20, 21.54])
    opt_time.update({"Friday": [8, 19]})
    opt_time.update(dict.fromkeys(["Saturday", "Sunday"], [10, 18]))
    op_msg = []
    msg = ""
    for key in day_list:
        op_msg.append(util.get_time_des(key, opt_time))
    day = datetime.datetime.today().weekday()
    time_list = opt_time[day_list[day]]
    if len(time_list) == 2:
        hours = datetime.datetime.today().now().hour
        if time_list[0] <= hours < time_list[1]:
            msg = "Now the library is open."
        else:
            msg = "Now the library is closed."
    if len(time_list) == 4:
        hours = datetime.datetime.today().now().hour
        print(hours)
        if time_list[0] <= hours < time_list[1] or time_list[2] <= hours < time_list[3]:
            msg = "Now the library is open."
        else:
            msg = "Now the library is closed."

    return render(request, 'libapp/About.html',
                  {'msg': msg, 'op_msg': op_msg, 'cookie_msg': request.COOKIES['about_visits']})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            province = form.cleaned_data['province']
            phone = form.cleaned_data['phone']
            postal_code = form.cleaned_data['postal_code']
            photo = form.cleaned_data['photo']

            if LibUser.objects.get_or_create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    email=email,
                    address=address,
                    city=city,
                    province=province,
                    phone=phone,
                    postal_code=postal_code,
                    photo=photo):
                return render(request, 'libapp/Success.html')
            else:
                return render(request, 'libapp/Fail.html', {'msg': "User already existed."})
    else:
        form = RegisterForm()
    return render(request, 'libapp/Register.html', {'form': form})


def user_login(request):

    rd = random.randint(1, 9)
    request.session['lucky_num'] = rd
    request.session.set_expiry(3600)

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'libapp/Login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return render(request, 'libapp/Index.html')
            else:
                return render(request, 'libapp/Login.html', {'form': form, 'password_is_wrong': True})
        else:
            return render(request, 'libapp/Login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'libapp/Index.html')


def check_login(request):
    if not request.user.is_authenticated():
        return render(request, 'libapp/Index.html', {'log_msg': 'Please login first'})
    else:
        return None


def data_manage(request):
    return render(request, 'libapp/DataManage.html')


def data_export(request):
    if util.export_data():
        return render(request, 'libapp/DataManage.html', {'log_msg': 'Data Export!'})
    else:
        return render(request, 'libapp/DataManage.html', {'log_msg': 'Export Error!!'})
