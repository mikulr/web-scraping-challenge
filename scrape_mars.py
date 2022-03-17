from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import pandas as pd
from pretty_html_table import build_table


def scrape_info():
    #NEWS 
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    results=soup.find('div', class_="slide")

    news_title =results.find('div', class_="content_title").text
    news_p =results.find('div', class_='rollover_description_inner').text
    
    # FEATURED IMAGE
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)          

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    
    soup = bs(html, 'html.parser')
    img_url = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = (f"https://spaceimages-mars.com/{img_url}")

    #MARS FACTS
    url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url)

    df = tables[0]
    df.columns = ['Statistic', 'Mars', 'Earth']
    df = df.iloc[1:]
    del df['Earth']
    df=df.set_index("Statistic")
   
    df2= tables[1]
    df2.columns=['Statistic', 'Mars']
    df2=df2.set_index("Statistic")

    frames = [df, df2]
    result = pd.concat(frames)
    result.index.name = None

    mars_facts = build_table(result, 'green_dark', index=True, width='auto')

    #HEMISPHERES
    url = 'https://marshemispheres.com'
    response = requests.get(url)
    soup = bs(response.text, "html.parser") 

    response = soup.find_all('div', class_='item') 

    hemisphere_image_urls=[]

    for x in response:
        title= x.h3.text
        base_link=x.find('img', class_="thumb")['src']
        strp_link= base_link[40:]
        fix_link= strp_link.rstrip("_thumb.png")
        img_url=(f"https://marshemispheres.com/images/{fix_link}")
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p, 
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
        }

    # Return results
    return mars_data