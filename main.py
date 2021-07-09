import requests
from requests_html import HTML
from requests_html import HTMLSession
import pandas as pd
import xml.etree.ElementTree as et

# enter url

urls = input("please enter a urls separed them using space or comma :  \n\n")
print("your url is her", urls)

def validator_urls(all_urls):
    errors_tabs = []
    tab_urls = all_urls.split()
    for url in tab_urls:
        ary = url.split(": ")
        if ary[0] != 'https' and ary[0] != 'http':
            el = {ary[0]: "this Url is invalid"}
            errors_tabs.append(el)
    return errors_tabs


def get_source_code(base_url):
    try:
        session = HTMLSession()
        response = session.get(base_url)  # get the response
        return response
    except requests.exceptions.RequestException as e:
        print(e)


def parse_data(xml):
    try:
        tree = et.parse(xml)
        root = tree.getroot()
        return root
    except et.ParseError as e:
        print("Error while parsing xml: " + xml + "\n Exception: " + e)


def get_feed(array_urls):
    error = validator_urls(array_urls)
    if len(error) > 0:
        raise ValueError(error)

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
    return definition


df = get_feed(urls)
df.head()
