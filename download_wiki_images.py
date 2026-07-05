import urllib.request
import urllib.parse
import json
import os

queries = {
    'mq135': 'MQ-135',
    'lm386': 'LM386',
    'hx711': 'HX711',
    'loadcell': 'Load cell',
    'ssr': 'Solid-state relay'
}

def get_wikimedia_image(query, filename):
    try:
        # Search for page
        url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=' + urllib.parse.quote(query) + '&utf8=&format=json'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        
        if not res['query']['search']:
            print(f'No Wikipedia page for {query}')
            return False
            
        page_title = res['query']['search'][0]['title']
        
        # Get page images
        url = 'https://en.wikipedia.org/w/api.php?action=query&titles=' + urllib.parse.quote(page_title) + '&prop=images&format=json'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        
        pages = res['query']['pages']
        page_id = list(pages.keys())[0]
        
        if 'images' not in pages[page_id]:
            print(f'No images found on page for {query}')
            return False
            
        for img in pages[page_id]['images']:
            img_title = img['title']
            if img_title.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Get image url
                url = 'https://en.wikipedia.org/w/api.php?action=query&titles=' + urllib.parse.quote(img_title) + '&prop=imageinfo&iiprop=url&format=json'
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
                
                img_pages = res['query']['pages']
                img_page_id = list(img_pages.keys())[0]
                img_url = img_pages[img_page_id]['imageinfo'][0]['url']
                
                print(f'Downloading {img_url} for {filename}')
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(req, timeout=10).read()
                with open(filename, 'wb') as f:
                    f.write(img_data)
                print(f'Saved {filename}')
                return True
                
    except Exception as e:
        print(f'Search failed for {query}: {e}')
    return False

for name, query in queries.items():
    get_wikimedia_image(query, f'images/{name}.jpg')
