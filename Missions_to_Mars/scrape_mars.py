from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pymongo
import requests



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit Mars webpage 1 - MARS NEWS ------------------------------------
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into soup, parse with html.parser 
    html = browser.html
    soup = bs(html, 'html.parser')

    # Chain .find to find the first title of the first new article
    first_title = soup.find('li', class_="slide").find('div', class_="content_title").text

    # Chain .find to find the first paragraph of the first new article
    first_paragraph = soup.find('li', class_="slide").find('div', class_="article_teaser_body").text


    # Visit Mars webpage 2 - MARS FEATURED IMAGE ------------------------------------
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)


    # Visit Mars webpage 3 - MARS WEATHER ------------------------------------
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)

    tweet_text_xpath = '//*[@id="react-root"]/div/div/div/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div/div[1]/div/article/div/div[2]/div[2]/div[2]/span'
    weather_tweet = browser.find_by_xpath(tweet_text_xpath)
    mars_weather = weather_tweet.text


    # Visit Mars webpage 4 - MARS FACTS------------------------------------
    url = 'https://space-facts.com/mars/'
    
    # Get list of tables on the webpage
    tables = pd.read_html(url)

    # Get the first table 
    mars_facts_table = tables[0]
    mars_facts_table.columns = ['Features:', 'Stats:']

    # Create html table out of mars facts table
    html_table = mars_facts_table.to_html()


    # Visit Mars webpage 5 - MARS HEMISPHERES ------------------------------------
    # Cerberus Hemisphere 
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    cerberus = soup.find('section', class_='block metadata')
    cerberus_title = cerberus.find('h2', class_='title').text
    cerberus_link = cerberus.find('a')
    cerberus_url = cerberus_link['href']

    # Schiaparelli Hemisphere
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    schiaparelli = soup.find('section', class_='block metadata')
    schiaparelli_title = schiaparelli.find('h2', class_='title').text
    schiaparelli_link = schiaparelli.find('a')
    schiaparelli_url = schiaparelli_link['href']

    # Syrtis Major Hemisphere 
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    syrtis = soup.find('section', class_='block metadata')
    syrtis_title = syrtis.find('h2', class_='title').text
    syrtis_link = syrtis.find('a')
    syrtis_url = syrtis_link['href']

    # Valles Marineris Hemisphere 
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    valles = soup.find('section', class_='block metadata')
    valles_title = valles.find('h2', class_='title').text
    valles_link = valles.find('a')
    valles_url = valles_link['href']

    hemisphere_image_urls = [
    {"title": valles_title, "img_url": valles_url},
    {"title": cerberus_title, "img_url": cerberus_url},
    {"title": schiaparelli_title, "img_url": schiaparelli_url},
    {"title": syrtis_title, "img_url": syrtis_url},
    ]

    # Store data in a dictionary
    mars_data = {
        "News Title": first_title,
        "News Content": first_paragraph,
        "Mars Weather": mars_weather,
        "Mars Facts": html_table,
        "Mars Hemispheres": hemisphere_image_urls    
    }   

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
