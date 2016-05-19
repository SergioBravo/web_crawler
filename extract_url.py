#! usr/bin/env

def get_page(url):
	try:
		import urllib
		return urllib.urlopen(url).read()
	except:
		return ""

def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link < 0:
		return None, 0
	else:
		start_quote = page.find('"', start_link)
		end_quote = page.find('"', start_quote + 1)
		url = page[start_quote + 1:end_quote]
	return url, end_quote

def union(p, q):
	for e in q:
		if e not in p:
			p.append(e)

def crawl_web(seed, max_pages):
	tocrawl = [seed]
	crawled = []
	index = {}
	graph = {}
	while tocrawl:
		if max_pages == 0:
			return crawled
		page = tocrawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			
			union(tocrawl, outlinks)
			crawled.append(page)
		max_pages -= 1
	return index, graph

"""def crawl_web(seed,max_depth):
    tocrawl = [seed]
    crawled = []
    need_depth = []
    depth = 0
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            union(need_depth, get_all_links(get_page(page)))
            crawled.append(page)
        if not tocrawl:
            tocrawl, need_depth = need_depth, []
            depth += 1
    return crawled
"""

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

def add_to_index(index, keyword, url):
	if keyword in index:
		index[keyword].append(url)
	else:
		index[keyword] = [url]

def lookup(index, keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None

def add_page_to_index(index, url, content):
	words = content.split()
	for word in words:
		add_to_index(index, word, url)

index = crawl_web("https://en.wikipedia.org/wiki/Python", 30)
print index
word = lookup(index, 'https://en.wikipedia.org/wiki/Python')
print word