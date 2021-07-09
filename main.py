import requests
from requests_html import HTMLSession
import pandas as pd
import xml.etree.ElementTree as et
import re

# enter url

urls = input("please enter a urls separed them using space:  \n\n")
print("your url is her", urls)

def validator_urls(all_urls):
    errors_tabs = []
    tab_urls = all_urls.split()
    regex = re.compile(
        r'^(?:http)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    for url in tab_urls:
        errors_tabs.append({'url': re.match(regex, url) is not None})
    return errors_tabs



def get_source_code(base_url):
    try:
        session = HTMLSession()
        response = session.get(base_url)  # get the response
        return response
    except requests.exceptions.RequestException as e:
        print(e)


def get_feed(array_urls):
    errors_tabs = validator_urls(array_urls)
    for value in errors_tabs:
        print(value['url'])
        if value:
            # raise ValueError('Invalide Url', value)
            response = get_source_code(array_urls)
            definition = pd.DataFrame(columns=['title', 'links', 'pubDate', 'guid', 'description', 'meta'])
            with response as r:
                items = r.html.find("item", first=False)
                for item in items:
                    title = item.find('title', first=True).text
                    pubDate = item.find('pubDate', first=True).text
                    guid = item.find('guid', first=True).text
                    links = item.find('links', firts=True).text
                    row = {
                        'title': title,
                        'pubDate': pubDate,
                        'guid': guid,
                        'links': links
                    }
                    definition = definition.append(row, ignore_index=True)
        else:
            raise ValueError('Invalide Url', value)
    return definition


df = get_feed(urls)
df.head()