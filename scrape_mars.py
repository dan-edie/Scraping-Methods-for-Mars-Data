# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    """Scrape specific websites and return a dictonary of stored results"""
    mars_dict = {}
    browser = init_browser()
    
    ### Scraping NASA's news site for top Martian stories
    url = 'https://mars.nasa.gov/news/'

    # access the website and create a bs4 object
    browser.visit(url)
    time.sleep(4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_dict['news_title'] = soup.find_all('div', class_= 'content_title')[1].get_text()
    mars_dict['news_p'] = soup.find_all('div', class_= 'article_teaser_body')[0].get_text()

    ### Scraping JPL for featured Mars images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    time.sleep(4)

    # click to get to full size image
    browser.click_link_by_partial_text('FULL IMAGE')

    # second click
    browser.click_link_by_partial_text('more info')

    # scrape and find the image url
    html = browser.html
    time.sleep(4)
    soup = BeautifulSoup(html, 'html.parser')

    # create the image url string
    mars_dict['featured_image_url'] = 'https://www.jpl.nasa.gov' + soup.find('img', class_='main_image').get('src')

    ### Scraping Twitter for today's Martian Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(6)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    # Mars weather from most recent tweet
    try:
        mars_dict['mars_weather'] = soup.find_all(text=re.compile("InSight"))[0]
    except IndexError:
        print("Not Working")

    ### Scraping a website to pull a table of Mars facts
    tables = pd.read_html('https://space-facts.com/mars/')

    # create a dataframe from the table
    mars_df = tables[0]
    mars_df.columns = ['info', 'Value']
    mars_df = mars_df.set_index('info')
    mars_df.index.name = None
    
    # convert to HTML and drop any \n
    html_table = mars_df.to_html()
    mars_dict['html_table'] = html_table.replace('\n', '')

    ### Scraping the USGS astrogeoly site for hi-res Martain Hemisphere images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    time.sleep(4)
    soup = BeautifulSoup(html, 'html.parser')

    hemi_titles = []
    hemi_imgs = []

    # find the links on the page
    hemi_links = soup.find_all('div', class_='item')

    # getting the hemisphere names and storing them to a list
    for link in hemi_links:
        hemi_name = link.find('h3').get_text()
        hemi_titles.append(hemi_name)

    # for each title stored, click on the link associated
    for title in range(len(hemi_titles)):
        # links are available on each page, but might need to go to second link
        # on page. Finds the links or moves page forward to find
        try:
                browser.click_link_by_partial_text(hemi_titles[title])
        except:
                browser.find_link_by_text('2').first.click()
                time.sleep(4)
                browser.click_link_by_partial_text(hemi_titles[title])

        html = browser.html
        soup2 = BeautifulSoup(html, 'html.parser')
        hemi_soup = soup2.find('div', 'downloads')
        hemi_url = hemi_soup.a['href']

        # append the title and url to the dictionary
        hemi_dict={"title": hemi_titles[title].replace(' Enhanced', ''), 'img_url': hemi_url}
        hemi_imgs.append(hemi_dict)

    # append the dictionaries to the list
    mars_dict['hemi_imgs'] = hemi_imgs

    # close the browser
    browser.quit()
    
    return mars_dict