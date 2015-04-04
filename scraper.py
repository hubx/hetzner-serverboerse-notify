import subprocess
import json
import re
import time
import smtplib


def extract_offers(servers):
    interesting_offers = []
    for s in servers:
        s['cpu_b'] = int(s['cpu_b'])
        s['price'] = float(s['price'])
        s['ram'] = int(s['ram'])

        if s['cpu_b'] > 7960 and s['price'] <= 33.0 and s['ram'] >= 32:
            interesting_offers.append(s)
    return interesting_offers


def parse_interesting_offers(interesting_offers):
    return_in = 3600
    return_in_s = "1h"

    for s in interesting_offers:
        # parse next price reduction
        if s['reduction'] == "Fixed price":
            s['reduction_in_s'] = 24 * 3600
        elif "h" in s['reduction']:
            m = re.match(r"(?P<h>\d+)h (?P<m>\d+)m", s['reduction'])
            s['reduction_in_s'] = 3600 * int(m.group('h')) + 60 * int(m.group('m'))
        elif "<" in s['reduction']:  # less than 1 minute to price drop
            s['reduction_in_s'] = 30
        else:
            m = re.match(r"(?P<m>\d+)m", s['reduction'])
            s['reduction_in_s'] = 60 * int(m.group('m'))
        return_in = min(return_in, s['reduction_in_s'])
        return_in_s = s['reduction']
        del s['reduction_in_s']

        # parse offer id & URL
        m = re.match("javascript:expandBox\(this, 'market_details_(?P<id>\w+)', '(?P<url>[a-zA-Z0-9_/]+)'", s['id'])
        s['id'] = int(m.group('id'))
        s['url'] = "https://robot.your-server.de" + m.group('url')

    return return_in, return_in_s


def scrapy_crawl():
    process = subprocess.Popen(["scrapy", "crawl", "hetzner", "-o-", "-t", "json"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return json.loads(output.replace("[]", "").replace("][", ","))


def send_mail(offers, return_in):
    offers_string = ""
    for s in offers:
        offers_string += str(s) + "\n\n"

    msg = """From: Hetzner Notify <from@example.com>
To: interested party <to@example.com>
Subject: New offers on Hetzner, next reduction in {0:s}

{1:s}
""".format(return_in, offers_string)

    mail = smtplib.SMTP_SSL('smtp.example.com')
    mail.login('from@example.com', 'pass')
    mail.sendmail("from@example.com", ["to@example.com, to2@example.com"], msg)


if __name__ == "__main__":
    while 1:
        all_offers = scrapy_crawl()
        offers = extract_offers(all_offers)

        offers_in, offers_in_s = parse_interesting_offers(offers)
        if offers:
            #send_mail(offers, offers_in_s)
            print offers
        time.sleep(offers_in + 61)