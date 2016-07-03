import math
from django.core import serializers
from django.core.files import File
from libapp.models import User, LibUser, LibItem, Book, Dvd, Suggestion


def get_time_des(key, opt_time):

    res_str = ""
    time_list = opt_time[key]
    if len(time_list) == 2:
        res_str += key + " : " + to_12_hour(time_list[0]) + " - " + to_12_hour(time_list[1])
    if len(time_list) == 4:
        res_str += key + " : " + to_12_hour(time_list[0]) + " - " + to_12_hour(time_list[1]) + " & " + \
                   to_12_hour(time_list[2]) + " - " + to_12_hour(time_list[3])
    return res_str


def to_12_hour(time):

    str_time = ""
    if 0 <= time <= 12:
        str_time = str(math.trunc(time)) + ":" + str(round((time - int(time)) * 100))[:2].zfill(2) + " am"
    else:
        str_time = str(math.trunc(time)) + ":" + str(round((time - int(time)) * 100))[:2].zfill(2) + " pm"
    return str_time


def export_data():

        all_objects = list(User.objects.all()) + list(LibUser.objects.all()) + list(LibItem.objects.all()) \
                      + list(Book.objects.all()) + list(Dvd.objects.all()) + list(Suggestion.objects.all())
        print(all_objects)
        data = serializers.serialize('json', all_objects)
        print(data)
        with open('libapp/db_dump/data.json', 'w') as f:
            my_file = File(f)
            my_file.write(data)
        return True


