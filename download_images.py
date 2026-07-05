import urllib.request
import re
import os

queries = {
    'mq135': 'MQ135 gas sensor module arduino',
    'lm386': 'LM386 sound sensor module arduino',
    'hx711': 'HX711 load cell amplifier module',
    'loadcell': '10kg aluminum load cell',
    'ssr': 'solid state relay module arduino'
}

def get_image(query, filename):
    try:
        url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query + ' images')
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Duckduckgo html image search doesn't show direct images easily, let's just use Yahoo Image Search
        url = 'https://images.search.yahoo.com/search/images?p=' + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        img_urls = re.findall(r'imgurl=&quot;(http[^&]+)&quot;', html)
        if not img_urls:
            img_urls = re.findall(r'src=\'(http[^\']+)\'', html)
            
        for img_url in img_urls:
            try:
                print(f'Downloading {img_url} for {filename}')
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(req, timeout=5).read()
                with open(filename, 'wb') as f:
                    f.write(img_data)
                print(f'Saved {filename}')
                return
            except Exception as e:
                print(f'Failed {img_url}: {e}')
    except Exception as e:
        print(f'Search failed for {query}: {e}')

for name, query in queries.items():
    get_image(query, f'images/{name}.jpg')
