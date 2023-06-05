from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET
import urllib.request as urllib2
import shutil
from xml.etree.ElementTree import parse
import feedparser
from xml.etree import ElementTree 
from lxml import etree
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
prefs = {
'download.default_directory': 'C:/Utility/Downloads/',
'download.prompt_for_download': False,
'download.extensions_to_open': 'xml',
'safebrowsing.enabled': True
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs',prefs)
options.add_argument('--headless')
# options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--safebrowsing-disable-download-protection")
options.add_argument("safebrowsing-disable-extension-blacklist")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

with open('urls.txt', 'r') as f:
    urls = f.readlines()


  
def xmlProcess(url, titles, contents, descriptions, xml_urls):
    driver.get(url)
    parser = etree.XMLParser(recover=True, encoding='iso-8859-5')
    data = driver.find_element("xpath","/html/body").text
    xml_root = ElementTree.fromstring(data, parser=parser)
    items = xml_root.findall('channel/item')
    #print(items[0])
    for i in range(len(items)):   
        title = items[i].findtext('.//title')  
        content = items[i].findtext('{http://purl.org/rss/1.0/modules/content/}encoded') 
        description = items[i].findtext('description')
        titles.append(title)
        contents.append(content)
        descriptions.append(description)
        xml_urls.append(url)
    return titles, contents, descriptions, xml_urls

if __name__ == '__main__':
    titles, contents, descriptions, xml_urls = [], [], [], []
    for url in urls: 
        try: 
            titles, contents, descriptions, xml_urls = xmlProcess(url.replace('\n', ''), titles, contents, descriptions, xml_urls)
        except Exception as e:
            pass

    df = pd.DataFrame(list(zip(xml_urls, titles, descriptions, contents)),
                columns =['url', 'title', 'descriptions', 'contents'])

    df.to_csv('results_vf.csv', index=False)