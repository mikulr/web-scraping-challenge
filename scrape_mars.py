from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo


def scrape_info():
    #The url link in the homework is maybe wrong?  
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)

    #make the soup
    soup = bs(response.text, 'html.parser')

    results=soup.find('div', class_="slide")

    news_title =results.find('div', class_="content_title").text
    news_p =results.find('div', class_='rollover_description_inner').text

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)          

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    img_url = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = (f"https://spaceimages-mars.com/{img_url}")

   
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p, 
        "featured_image_url": featured_image_url
        }

   

    # Return results
    return mars_data