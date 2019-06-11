from modules import file_io
import difflib, whois, re, urllib.request
from datetime import datetime
import pycurl, requests
import bs4

def ts(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def whois_(url):
    try:
        w = whois.whois(url)
        if(w.creation_date is not None):
            days_since = (datetime.now() - w.creation_date)
        else:
            return 0
        return days_since.days
    except Exception as e:
        return e

def shortened(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    return 1 if match else 0

def ssl(url):
    if (url[0:8] == "https://"):
        return 1
    else:
        return 0 


def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    return 1 if match else 0
    
def alexa(url):
    try:
        rank = bs4.BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find(
                "POPULARITY")['TEXT']
        return int(rank)
    except Exception as e:
        return 0

def check_extension(url):
    if(re.search("edu.tr", url)):
        return 1
    elif(re.search("gov.tr",url)):
        return 1
    else:
        return 0

def domain_analysis(url):
    whitelist = file_io.read("safe_keywords")
    is_shortened = shortened(url)
    has_ip = having_ip_address(url)
    has_ssl = ssl(url)
    alexa_rank = alexa(url)
    domain_age = whois_(url)
    try:
        domain_age = int(domain_age)
    except Exception as e:
        domain_age = 0
    special_domain = check_extension(url)
    ts_max = 0
    t = ""
    
    dom = url.split("//")
    if(len(dom) > 1):
        subdom = dom[1].split(".")
        subdom = subdom[:-1]
    
        for i in subdom:
            words = i.split('-')
            for word in words:
                for j in whitelist:
                    ts_score = ts(word,j)
                    if(ts_score > ts_max):
                        ts_max = ts_score 
                        t = j

    result = [domain_age, has_ip, is_shortened, alexa_rank, special_domain, ts_max]
    return result
