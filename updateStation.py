#!/usr/bin/env python

import re
import requests
import urllib3

pattern = u"([\u4e00-\u9fa5]+)\|([A-Z]+)"

def station_dict():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    webpage_url = "https://kyfw.12306.cn/otn/leftTicket/init"
    webpage = requests.get(webpage_url)
    webpage_text = webpage.text
    webpage_parts = webpage_text.split("\"")
    for part in webpage_parts:
        if part.startswith("/otn/resources/js/framework/station_name.js?station_version="):
            station_url = "https://kyfw.12306.cn" + part
            station_page = requests.get(station_url, verify=False)
            result = re.findall(pattern, station_page.text)
            return dict(result)

