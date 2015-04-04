# hetzner-serverboerse-notify
Scrape and filter the hetzner serverboerse with [Scrapy](http://scrapy.org/). Notify via email

I wanted to plot server on hetzner's serverboerse over time. This turned into a simple email notifier, but all the requirements are there. (Somebody has to move the parser logic in `scraper.py` to scrapies Item Pipeline)

Feel free to use this as a template for your own scrape and notify script :)

## Run
```
$ pip install scrapy
$ python scaper.py
```
