import datetime
from django.http import HttpResponse
from libapp.util import util
from libapp.models import User
from django.shortcuts import render
from django.shortcuts import render_to_response
from libapp.util.forms import RegisterForm
from libapp.models import Libitem, Libuser, Dvd, Book,Suggestion
from django.shortcuts import get_list_or_404
from libapp.forms import SuggestionForm,SearchLibForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.

def searchlib(request):
    form = SearchLibForm()
    return render(request, 'libapp/searchresult.html', {'form':form})


def searchresult(request):
    results = []
    error = ""
    if request.method == 'POST':
        form = SearchLibForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            name = form.cleaned_data['name']
            if(title or name):
                result1 = Book.objects.filter(Q(title__contains=title)|Q(author__contains=name))
                result2 = Dvd.objects.filter(Q(title__contains=title)|Q(maker__contains=name))
                results.extend(result1)
                results.extend(result2)
                return render(request, 'libapp/searchresult.html', {'form':form, 'results':results,'error':error})
            else:
                error = "please input at lease one"
                return render(request, 'libapp/searchresult.html', {'form':form, 'results':results,'error':error})
    else:
        form = SearchLibForm()
    return render(request, 'libapp/searchresult.html', {'form':form, 'results':results,'error':error})

def suggestions(request):
    suggestion_list =Suggestion.objects.all()
    return render(request, 'libapp/suggestions.html', {'suggestion_list': suggestion_list})

def newitem(request):
    suggestion_list2 =  Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('libapp:suggestions'))
        else:
            return render(request, 'libapp/newitem.html', {'form':form, 'suggestion_list2':suggestion_list2})
    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form':form, 'suggestion_list2':suggestion_list2})


def details(request, item_id):
    items = get_list_or_404(Libitem,id=item_id)
    for item in items:
        if item.itemtype == 'Book':
            result = get_list_or_404(Book,id=item_id)
        else:
            result = get_list_or_404(Dvd,id=item_id)
    return render(request, 'libapp/details.html', {'result': result})


def index(request):
    return render(request, 'libapp/index.html')


def books(request):
    book_list = Book.objects.all().order_by("-pubyr")[:10]
    return render(request, 'libapp/books.html', {'book_list': book_list})


def dvds(request):
    dvd_list = Dvd.objects.all().order_by("-pubyr")[:10]
    return render(request, 'libapp/dvds.html', {'dvd_list': dvd_list})


def others(request):
    other_list = ["Other_" + str(x) for x in range(1,20)]
    return render(request, 'libapp/others.html', {'other_list': other_list})


def my_acct(request):
    msg = "Hello User!"
    return render(request, 'libapp/myacct.html', {'msg': msg})


def base(request):
    return render(request, 'libapp/MainBase.html')


def about(request):
    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    opt_time = dict.fromkeys(["Monday", "Tuesday", "Wednesday", "Thursday"], [8.30, 12, 13.20, 21.54])
    opt_time.update({"Friday": [8, 19]})
    opt_time.update(dict.fromkeys(["Saturday", "Sunday"], [10, 18]))
    opMsg = []
    for key in day_list:
        opMsg.append(util.get_time_desp(key, opt_time))
    day = datetime.datetime.today().weekday()
    time_list = opt_time[day_list[day]]
    if len(time_list) == 2:
        hours = datetime.datetime.today().now().hour
        if time_list[0] <= hours < time_list[1]:
            msg = "Now the library is open."
        else:
            msg = "Now the library is closed."
    if len(time_list) == 4:
        hours = datetime.datetime.today().now()
        print(hours)
        if time_list[0] <= hours < time_list[1] or time_list[2] <= hours < time_list[3]:
            msg = "Now the library is open."
        else:
            msg = "Now the library is closed."
    return render(request, 'libapp/about.html', {'msg': msg, 'opMsg': opMsg})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            if User.objects.get_or_create(f_name=f_name, l_name=l_name, email=email, gender=gender)[1]:
                return render_to_response('libapp/success.html')
            else:
                return render_to_response('libapp/fail.html', {'msg': "User already existed."})
    else:
        form = RegisterForm()
    return render(request, 'libapp/register.html', {'form': form})
