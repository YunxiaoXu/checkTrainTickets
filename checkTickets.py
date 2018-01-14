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

dongche         = False
gaotie          = False
tekuai          = False
kuaisu          = False
zhida           = False
from_station    = ""
to_station      = ""
date            = "" 
new_coding      = "gbk" if platform.system()=="Windows" else "utf-8"
stations        = updateStation.station_dict()
istations       = {v:k for k,v in stations.items()}

def usage():
    print(__doc__).encode(new_coding)
    sys.exit(0)

def getInfo():
    global dongche
    global gaotie
    global tekuai
    global kuaisu
    global zhida
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
            dongche = True
        elif o in ("-G", "--Highspeed"):
            gaotie = True
        elif o in ("-T", "--Express"):
            tekuai = True
        elif o in ("-K", "--Fast"):
            kuaisu = True
        elif o in ("-Z", "--Direct"):
            zhida = True
        elif o in ("-f", "--from"):
            from_station = stations.get(a.decode(new_coding)) or None
        elif o in ("-t", "--to"):
            to_station = stations.get(a.decode(new_coding)) or None
        elif o in ("-d", "--date"):
            date = a.decode(new_coding)
        else:
            assert False, "Unhandled Option"

    if not (dongche or gaotie or tekuai or kuaisu or zhida):
        dongche = gaotie = tekuai = kuaisu = zhida = True

    if not from_station or not to_station:
        print "Station not available."
        sys.exit(0)

def getData():
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
        print u"{no: <6} {f} {t} {st},{at} {td} {y} {e}".format(\
                no=train_no, f=ch(from_station_name,8), t=ch(to_station_name,8), st=start_time,
                at=arrive_time, td=time_duration, y=ch(first_class_seat,3), e=ch(second_class_seat,3)\
                ).encode(new_coding)


if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    getInfo()
    getData()
