import datetime
from googlesearch import search, get_tbs

def do_google_search(query, date = None):
    timeframe = None
    if date:
        to_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        from_date = to_date - datetime.timedelta(days=2)
        timeframe = get_tbs(from_date, to_date)
    query_results = []
    for j in search(query, tld="co.in", num=10, stop=10, pause=2, tbs=timeframe):
        query_results.append(j)
    return query_results

def parse_html_page(html_links):
    pass

