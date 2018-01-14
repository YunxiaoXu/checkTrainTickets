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
import platform

dongche         = False
gaotie          = False
tekuai          = False
kuaisu          = False
zhida           = False
from_station    = ""
to_station      = ""
date            = "" 
new_coding      = "gbk" if platform.system()=="Windows" else "utf-8"

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
            from_station = a.decode(new_coding)
        elif o in ("-t", "--to"):
            to_station = a.decode(new_coding)
        elif o in ("-d", "--date"):
            date = a.decode(new_coding)
        else:
            assert False, "Unhandled Option"

    if not (dongche or gaotie or tekuai or kuaisu or zhida):
        dongche = gaotie = tekuai = kuaisu = zhida = True

def getData():
    global from_station
    global to_station
    global date

    url_template = (
        "https://kyfw.12306.cn/otn/leftTicket/queryZ?"
        "leftTicketDTO.train_date={date}&"
        "leftTicketDTO.from_station={from_station}&"
        "leftTicketDTO.to_station={to_station}&"
        "purpose_codes=ADULT"
    )

    request_url = url_template.format(from_station=from_station, to_station=to_station, date=date)

    data = requests.get(request_url)
    
    print data.text.encode(new_coding)

if __name__ == "__main__":
    getInfo()
    print u"动车：{}".format(dongche).encode(new_coding)
    print u"高铁：{}".format(gaotie).encode(new_coding)
    print u"特快：{}".format(tekuai).encode(new_coding)
    print u"快速：{}".format(kuaisu).encode(new_coding)
    print u"直达：{}".format(zhida).encode(new_coding)
    print u"出发：{}".format(from_station).encode(new_coding)
    print u"抵达：{}".format(to_station).encode(new_coding)
    print u"日期：{}".format(date).encode(new_coding)
    getData()
