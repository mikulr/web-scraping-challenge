from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import pandas as pd


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
   
    df2= tables[1]
    df2.columns=['Statistic', 'Mars']

    frames = [df, df2]
    result = pd.concat(frames,ignore_index=True)
    
    mars_facts = result.to_dict('records')

    #HEMISPHERES
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)  
    
    url = 'https://marshemispheres.com'
    browser.visit(url)
    response = requests.get(url)
    soup = bs(response.text, "html.parser") 

    response = soup.find_all('div', class_='item') 

    hemisphere_image_urls=[]

    for x in response:
        
         #using soup grab title 
        title= x.h3.text
        #find  page with image
        links= x.find("a", class_="itemLink product-item")['href']
        browser.visit(f"https://marshemispheres.com/{links}")
        #find the link
        img_url = browser.find_by_text('Sample')['href']
        #append to dict
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})

    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p, 
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls, 
        "mars_facts": mars_facts

    }

    browser.quit()

    # Return results
    return mars_data