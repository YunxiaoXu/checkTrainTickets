#!/usr/bin/env python
#coding: utf-8
"""
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

dongche         = False
gaotie          = False
tekuai          = False
kuaisu          = False
zhida           = False
from_station    = ""
to_station      = ""
date            = ""

def usage():
    print(__doc__)
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
            ["help","Bullet","Highspeed","Express","Fast","Direct","from","to","date"]
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
            from_station = a
        elif o in ("-t", "--to"):
            to_station = a
        elif o in ("-d", "--date"):
            date = a
        else:
            assert False, "Unhandled Option"

if __name__ == "__main__":
    getInfo()