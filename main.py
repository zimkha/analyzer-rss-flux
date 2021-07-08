import feedparser

d = feedparser.parse('https://www.cert.ssi.gouv.fr/alerte/feed/')

print(d.feed)

print("Feed Title:", d.feed.title)
print("Feed Subtitle:", d.feed.subtitle)
