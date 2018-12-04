import scrapy
import json

# HOWTO
# set USER_AGENT and ROBOTSTXT_OBEY in settings.py
# set an instagram username in the script

class InstaSpider(scrapy.Spider):
    name = "insta"

    def start_requests(self):
        username = "benistenes"
        urls = [
            'https://www.instagram.com/' + username + '/?hl=en'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #with open("insta.txt", 'wb') as f:
        #    f.write(response.body)
        with open("insta_locations.txt", 'w') as f:
            f.write("Location\r\n")
        shortcodes = response.xpath('string(//body)').re(r'\"shortcode\":\"(\w+)\"')
        for shortcode in shortcodes:
            yield scrapy.Request("https://www.instagram.com/p/"+shortcode+"/?__a=1", callback=self.parse_post)
        
    def parse_post(self, response):
        graphql = json.loads(response.text)
        location = graphql['graphql']['shortcode_media']['location']
        if location != None:
            location_name = location.get('name', "")
            with open("insta_locations.txt", 'a+') as f:
                f.write(location_name + "\r\n")
