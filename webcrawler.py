
import time
import re
import requests

def get_page(url):
  try:
    html = requests.get(url).text
    # REGEX that removes HTML tags from content
    html_result = re.sub(r'^<\w+>+|<\D.*>+', '',   html)
    return html_result
  except:
    return ""

def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    return None


def add_to_index(index,keyword,url):
    if keyword in index:
      index[keyword].append(url)
    else:
      index[keyword] = [url]

def add_page_to_index(index,url,content):
    words_split = content.split()
    for word in words_split:
        add_to_index(index, word, url)


def get_next_target(page):
  start_link = page.find('<a href=')
  if start_link == -1:
    return None, 0

  start_quote = page.find('"', start_link)
  end_quote = page.find('"', start_quote + 1)

  url = page[start_quote + 1:end_quote]
  
  return url, end_quote
  
def get_all_links(page):
  links = []
  while True:
    url, end_pos = get_next_target(page)
    if url:
      links.append(url)
      page = page[end_pos:]
    else:
      break

  return links

def union(a, b):
  mylist = [e for e in b if e not in a]


def crawl_web(seed):
    tocrawl = [seed]
    print("this is tocrawl: ", tocrawl)
    crawled = []
    print(f"this is crawled {crawled}")
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        print("this is page in tocrawl while loop: ", page)
        if page not in crawled:
            print(f"{page} not in crawled")
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
            print(f"this is crawled last {crawled}")
      
    return index


print(lookup(crawl_web("https://www.espn.com/"), "the"))