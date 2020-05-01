from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': '/bin/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    #mars news
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    news_title = soup.find('div', class_= 'content_title').text
    news_p = soup.find('div', class_= 'rollover_description_inner').text

    #feature image
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    browser.click_link_by_partial_text('.jpg')

    featured_image_url = browser.url

    #Mars Weather
    twitter = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitter)
    soup = bs(response.text, 'lxml')

    results = soup.find_all('div', class_='js-tweet-text-container')
    mars_weather = results[2].text
    mars_weather = mars_weather.replace('\n','')
    

    #Hemisphere images
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_image_url = [
                       {'title':'Cerberus Hemisphere Enhanced', 'img_urls':''},
                       {'title':'Schiaparelli Hemisphere Enhanced', 'img_urls':''},
                       {'title':'Syrtis Major Hemisphere Enhanced', 'img_urls':''},
                       {'title':'Valles Marineris Hemisphere Enhanced', 'img_urls':''}
                       ]

    for x in range(0, 4):
        browser.visit(hemisphere_url)
        try:
            browser.click_link_by_partial_text(hemisphere_image_url[x]['title'])
            response = requests.get(browser.url)
            soup = bs(response.text, 'lxml')
            link = soup.find('li')
            img_link = link.find('a')
            i_links = img_link['href']
            hemisphere_image_url[x]['img_urls'] = i_links
        except:
            print('...')


    mars_data = {
                'news_title': news_title,
                'news_p': news_p,
                'feature_img_url': featured_image_url,
                'mars_weather': mars_weather,
                'hemisphere_img': hemisphere_image_url
                }
    browser.quit()
    return mars_data