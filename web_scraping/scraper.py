import os
import json
import datetime
from googlesearch import search, get_tbs
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

def do_google_search(query, date = None):
    timeframe = None
    if date:
        to_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        from_date = to_date - datetime.timedelta(days=2)
        timeframe = get_tbs(from_date, to_date)
    query_results = []
    for j in search(query, tld="co.in", num=2, stop=3, pause=2, tbs=timeframe):
        query_results.append(j)
    return query_results

def parse_html_page(html_link):
    print('page parsing:', html_link + '...')
    try:
        res = requests.get(html_link, timeout=5)
    except:
        print('WARNING! Request timed out:','Could not process request to', html_link)
        return None
    html_page = res.content
    try:
        soup = BeautifulSoup(html_page, 'html.parser')
    except:
        print('Parsing failed:', html_link)
        return None
    text = soup.find_all(text=True)
    print('found all text on page')
    important_text = []
    links = []
    for elem in text:
        if (len(elem) > 200 and '{' not in elem and '}' not in elem and
           '=' not in elem and "\"(" not in elem and "\")" not in elem and
           '<' not in elem and '>' not in elem):
            if 'https://' in elem:
                link_start = elem.find('https://')
                link_end = elem[link_start:].find(' ')
                link = elem[link_start : link_end]
                print('Found a link!', link)
                links.append(link)
            if 'http://' in elem:
                print('Found a link!', elem)
                link_start = elem.find('http://')
                link_end = elem[link_start:].find(' ')
                link = elem[link_start : link_end]
                print('Found a link!', link)
                links.append(link)
            removal_list = ['\n', '\t', '\u00a0', '\u201c']
            for char in removal_list:
                elem = elem.strip(char)
            if len(elem) > 200:
                sentences  = re.split("\\.\\s", elem)
                for sentence in sentences:
                    important_text.append(sentence)

    print('page parsed:', html_link)
    return {'text': important_text, 'links': links}

def create_stock_news_data(symbol, output_path, site_list, dates):
    
    for date in dates:
        full_info = {}
        query_results = {}
        for search_site in site_list:
            try:
                query_results[search_site] = do_google_search(symbol + ' stock news ' + search_site, date)
            except:
                print('WARNING: Google search', symbol + ' stock news ' + search_site, ' \nfor date:', date, '\nFAILED!!!!!!!!!')

        google_output_file = os.path.join(output_path, symbol + 'google_search_' + date + '.txt')

        with open(google_output_file, 'w') as outfile:
            pprint(query_results, stream=outfile)
        info = {}
        for key in query_results:
            info[key] = {}
            for site in query_results[key]:
                site_info = parse_html_page(site)
                if site_info:
                    info[key][site] = site_info
        full_info[date] = info
        if not os.path.exists(os.path.join(output_path, 'site_info.json')):
            with open(os.path.join(output_path, 'site_info.json'), 'w') as outfile:
                json.dump(full_info, outfile, indent=4)
        else:
            with open(os.path.join(output_path, 'site_info.json'), 'r') as json_file:
                data = json.load(json_file)
                data[date] = full_info[date]
            with open(os.path.join(output_path, 'site_info.json'), 'w') as json_file:
                json.dump(data, json_file, indent=4)