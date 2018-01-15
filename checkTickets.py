#!/usr/bin/env python
#coding: utf-8
u"""
Train Tickets Checking Tool

Usage:
    ./checkTickets.py [-dgktz] <date> <to> <date>

Options:
    -h --help                show help message
    -D --Bullet              Bullet Train
    -G --Highspeed           High-speed Rail
    -T --Express             Express Train
    -K --Fast                Fast Train
    -Z --Direct              Direct Train
    -f --from                Departure Station
    -t --to                  Arrival Station
    -d --date                Departure Date

Example:
    ./checkTickets.py -D -f 上海 -t 北京 -d 2018-01-13
    ./checkTickets.py --Bullet --from=上海 --to=北京 --date=2018-01-03
"""
import sys
import getopt
import requests
import urllib3
import platform
import updateStation

category        = []
All             = False
from_station    = ""
to_station      = ""
date            = "" 
new_coding      = "gbk" if platform.system()=="Windows" else "utf-8"
stations        = updateStation.station_dict()
istations       = {v:k for k,v in stations.items()}

def usage():
    print(__doc__).encode(new_coding)
    sys.exit(0)

def ch(ustr, slen, filling=' '):
    ulen = 0
    for ubyte in ustr:
        if u'\u4e00' <= ubyte <= u'\u9fa5':
            ulen += 2
        else:
            ulen += 1
    flen = max(0, slen-ulen)
    return ustr + filling*flen

def getInfo():
    global category
    global All
    global from_station
    global to_station
    global date

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hDGTKZf:t:d:",
            ["help","Bullet","Highspeed","Express","Fast","Direct","from=","to=","date="]
        )
    except getopt.GetoptError,e:
        print(str(e))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-D", "--Bullet"):
            category.append(u'D')
        elif o in ("-G", "--Highspeed"):
            category.append(u'G')
        elif o in ("-T", "--Express"):
            category.append(u'T')
        elif o in ("-K", "--Fast"):
            category.append(u'K')
        elif o in ("-Z", "--Direct"):
            category.append(u'Z')
        elif o in ("-f", "--from"):
            from_station = stations.get(a.decode(new_coding)) or None
        elif o in ("-t", "--to"):
            to_station = stations.get(a.decode(new_coding)) or None
        elif o in ("-d", "--date"):
            date = a.decode(new_coding)
        else:
            assert False, "Unhandled Option"

    if not category:
        All = True

    if not from_station or not to_station:
        print "Station not available."
        sys.exit(0)

def getData():
    global cattegory
    global All
    global from_station
    global to_station
    global date
    global istations
    global new_coding

    url_template = (
        "https://kyfw.12306.cn/otn/leftTicket/queryZ?"
        "leftTicketDTO.train_date={date}&"
        "leftTicketDTO.from_station={from_station}&"
        "leftTicketDTO.to_station={to_station}&"
        "purpose_codes=ADULT"
    )

    request_url = url_template.format(from_station=from_station, to_station=to_station, date=date)

    data = requests.get(request_url, verify=False)
    raw_trains = data.json()['data']['result']
    table_template = u"{} {} {} {} {} {} {} {}".format(
            ch(u'车次',6),
            ch(u'出发站',8),
            ch(u'到达站',8),
            ch(u'出发时间',8),
            ch(u'到达时间',8),
            ch(u'历时',6),
            ch(u'一等座',6),
            ch(u'二等座',6)
        )
    for raw_train in raw_trains:
        train = raw_train.split('|')
        train_no = train[3]
        from_station_code = train[6]
        to_station_code = train[7]
        start_time = train[8]
        arrive_time = train[9]
        time_duration = train[10]
        business_class_seat = train[32] or '--'
        first_class_seat = train[31] or '--'
        second_class_seat = train[30] or '--'
        advanced_soft_sleep = train[21] or '--'
        soft_sleep = train[23] or '--'
        hard_sleep = train[28] or '--'
        soft_seat = train[24] or '--'
        hard_seat = train[29] or '--'
        no_seat = train[26] or '--'
        from_station_name = istations.get(from_station_code)
        to_station_name = istations.get(to_station_code)
        if not All:
            if not (train_no[0] in category):
                continue
        table_template += u"\n{no} {f} {t} {st} {at} {td} {y} {e}".format(
                no=ch(train_no,6),
                f=ch(from_station_name,8),
                t=ch(to_station_name,8),
                st=ch(start_time,8),
                at=ch(arrive_time,8),
                td=ch(time_duration,6),
                y=ch(first_class_seat,6),
                e=ch(second_class_seat,6)
            )
    print table_template.encode(new_coding)


if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    getInfo()
    getData()
