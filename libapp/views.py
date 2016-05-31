import datetime
from libapp.util import util
from libapp.models import User
from django.shortcuts import render
from django.shortcuts import render_to_response
from libapp.util.forms import RegisterForm
# Create your views here.



def index(request):
    return render(request, 'libapp/index.html')


def books(request):
    book_list = ["Book_" + str(x) for x in range(1,20)]
    return render(request, 'libapp/books.html', {'book_list': book_list})


def dvds(request):
    dvd_list = ["DVD_" + str(x) for x in range(1,20)]
    return render(request, 'libapp/dvds.html', {'dvd_list': dvd_list})


def others(request):
    other_list = ["Other_" + str(x) for x in range(1,20)]
    return render(request, 'libapp/others.html', {'other_list': other_list})


def myacct(request):
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
        hours = datetime.now().hour
        if time_list[0] <= hours < time_list[1]:
            msg = "Now the library is open."
        else:
            msg = "Now the library is closed."
    if len(time_list) == 4:
        hours = datetime.datetime.now().hour
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
