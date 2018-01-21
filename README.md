# Train Tickets Checking Tool

**Check Train Tickets

The first project.

Check the train tickets left in China.
**

## Usage:
    ./checkTickets.py [-dgktz] <date> <to> <date>

## Options:
    -h --help                show help message
    -D --Bullet              Bullet Train
    -G --Highspeed           High-speed Rail
    -T --Express             Express Train
    -K --Fast                Fast Train
    -Z --Direct              Direct Train
    -f --from                Departure Station
    -t --to                  Arrival Station
    -d --date                Departure Date

## Example:
    ./checkTickets.py -D -f 上海 -t 北京 -d 2018-01-13
    ./checkTickets.py --Bullet --from=上海 --to=北京 --date=2018-01-03