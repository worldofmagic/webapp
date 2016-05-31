import math

def get_time_desp(key, opt_time):

    res_str = ""
    time_list = opt_time[key]
    if len(time_list) == 2:
        res_str += key + " : " + to_12_hour(time_list[0]) + " - " + to_12_hour(time_list[1])
    if len(time_list) == 4:
        res_str += key + " : " + to_12_hour(time_list[0]) + " - " + to_12_hour(time_list[1]) + " & " + \
                   to_12_hour(time_list[2]) + " - " + to_12_hour(time_list[3])
    return res_str

def to_12_hour(time):

    strTime = ""
    if 0 <= time <= 12:
        strTime = str(math.trunc(time)) + ":" + str(round((time - int(time)) * 100))[:2].zfill(2) + " am"
    else:
        strTime = str(math.trunc(time)) + ":" + str(round((time - int(time)) * 100))[:2].zfill(2) + " pm"
    return strTime

