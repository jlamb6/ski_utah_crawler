# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class SkiutahSpider(scrapy.Spider):
    name = 'skiutah'
    allowed_domains = ['https://www.skiutah.com/members/brighton/snowreport']
    time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    #custom_settings = {
    #    'FEED_URI': 'snow_conditions_%(time)s',
    #    'FEED_FORMAT': 'json'
    #}

    def start_requests(self):
        start_url = 'https://www.skiutah.com/members/__resort__/snowreport/'
        resorts = ["alta", "beaver-mountain", "brian-head", "brighton", "cherry-peak", "deer-valley", "eagle-point", "nordic-valley", "park-city", "powder-mountain", "snowbasin", "snowbird", "solitude", "sundance", "woodward-park-city"]
        for resort in resorts:
            url = start_url.replace('__resort__', resort)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        resort = response.url.split('/')[-3]
        resortName = resort.split('/')[0]

        snowfallContainer = response.css('div.su_temp-snowfall')
        snowfallLastDay = snowfallContainer.css('div.snowfall-24 div.amounts span::text').extract_first().strip()
        snowfallLastTwo = snowfallContainer.css('div.snowfall-history.hour48 div span::text').extract_first().strip()
        base = snowfallContainer.css('div.snowfall-history.base div span::text').extract_first().strip()
        ytd = snowfallContainer.css('div.snowfall-history.ytd div span::text').extract_first().strip()

        terrainContainer = response.css('div.su_card.resort-lifts')
        terrainInfo = terrainContainer.css('span.days::text').extract()
        runs = terrainInfo[0]
        lifts = terrainInfo[1]
        parks = terrainInfo[2]

        yield {
            'resort': resortName,
            '24hours': snowfallLastDay,
            '48hours': snowfallLastTwo,
            'base': base,
            'ytd': ytd,
            'runs': runs,
            'lifts': lifts,
            'parks': parks,
            'date': self.time
        }