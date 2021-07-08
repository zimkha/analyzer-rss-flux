import requests
from requests_html import HTML
from requests_html import HTMLSession
import pandas as pd
import xml.etree.ElementTree as et
# enter url
url = input("please enter a url :")
print("your url is her", url)


def validatorUrl (urls):
    return
def get_source_code(url: any):
    try:
        session = HTMLSession()
        response = session.get(url)  # get the response
        return response
    except requests.exceptions.RequestException as e:
        print(e)
def get_feed(url):
    array_split = url.split(":")
    if array_split[0] != 'https':
        raise NameError('Invalid url!')
    response = get_source_code(url)
    definition = pd.DataFrame(columns= ['title', 'links', 'pubDate', 'guid', 'description', 'meta'])
    with response as r:
        items = r.html.find("item", first=False)
        for item in items:
            title = item.find('title', first=True).text
            pubDate = item.find('pubDate', first=True).text
            guid = item.find('guid', first=True).text
            row = {
                   'title': title,
                   'pubDate': pubDate,
                   'guid': guid,
            }
            definition = definition.append(row, ignore_index=True)
    return definition


df = get_feed(url)
df.head()




