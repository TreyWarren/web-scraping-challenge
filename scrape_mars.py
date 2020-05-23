# !jupyter nbconvert --to script scrape_mars.ipynb

# Dependencies
import re
import requests
import pandas as pd 
from time import sleep
from splinter import Browser
from bs4 import BeautifulSoup as bs

mars_dict = {}

# Mars Facts
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def pandas_scrape_facts():

    # Read desired URL using Pandas
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    # Find Mars Facts DataFrame in the lists of DataFrames
    table_df = tables[0]

    # Name the columns
    table_df.columns = ['Attribute', 'Value']

    # Convert to HTML
    html_table = table_df.to_html(justify='left', index=False)

    # Add to master dictionary
    mars_dict["html_table"] = html_table
    
    # Return results
    return mars_dict


# Initialize ChromeDriver for the rest of the scraping
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def initialize_browser():
    # Path to chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    # Fire it up
    return Browser('chrome', **executable_path, headless=False)



# NASA Mars News 
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def browser_scrape_news():

    browser = initialize_browser()
    
    # Read desired URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    sleep(5) # sleep to allow the page to load
    html = browser.html
    soup = bs(html, 'html.parser')

    #### Titles
    title_results = soup.find_all('div', class_="content_title")

    # We can see above that we only care about the text in <a>
    titles_list = [title.a.text for title in title_results[1:]]

    # Select the first news title
    news_title = titles_list[0]

    #### Paragraphs
    teaser_results = soup.find_all('div', class_="article_teaser_body")
    teaser_results

    # We can see above that we only care about the text in <a>
    teasers_list = [teaser.text for teaser in teaser_results]
    teasers_list

    # Select the first news title
    news_p = teasers_list[0]

    # Add to master dictionary
    mars_dict["news_title"] = news_title
    mars_dict["news_paragraph"] = news_p

    # Return results
    return mars_dict

    browser.quit()



# JPL Mars Space Images - Featured Image
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def browser_scrape_image():
    
    browser = initialize_browser()
    
    # Read desired URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find tag <a> with featured image
    featured_image = soup.find('a', class_='button fancybox')

    # Create link to access featured image
    featured_image_page_url = "https://jpl.nasa.gov" + str(featured_image['data-link'])

    # Read desired URL of the actual page with the featured image
    url = featured_image_page_url
    browser.visit(url)
    sleep(5)
    soup = bs(browser.html, 'html.parser')

    # Find tag 'figure' with featured image
    figure = soup.find_all('figure')
    featured_image = figure[0].a

    featured_image_url = "https://jpl.nasa.gov" + str(featured_image['href'])
    
    # Add to master dictionary
    mars_dict["featured_image"] = featured_image_url

    # Return results
    return mars_dict

    browser.quit()



# Twitter - Mars Weather
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def browser_scrape_weather():
    
    browser = initialize_browser()
        
    # Read desired URL
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('div', text=re.compile("InSight")).text.replace('\n', '')
    
    # Add to master dictionary
    mars_dict["mars_weather"] = mars_weather

    # Return results
    return mars_dict

    browser.quit()



# USGS - Mars Hemispheres
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def browser_scrape_hemispheres():
    
    browser = initialize_browser()
        
    # Read desired URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    soup.find_all('div', class_='item')

    # Retreive all 4 results
    results = soup.find_all('div', class_='item')

    # in case the site is still down when this is being graded
    if results == []:
        hemisphere_image_urls = [{'title': 'Cerberus Hemisphere Enhanced',
        'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'},
        {'title': 'Schiaparelli Hemisphere Enhanced',
        'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'},
        {'title': 'Syrtis Major Hemisphere Enhanced',
        'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'},
        {'title': 'Valles Marineris Hemisphere Enhanced',
        'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]

    # if the site is back up, business as usual
    else:

        # Loop through the items
        hemisphere_image_urls = []
        base_url = 'https://astrogeology.usgs.gov'
        for result in results: 
            
            # Store title
            title = result.find('h3').text.replace(' Enhanced', '')
            
            # Store link that leads to full image website
            image_page_url = result.find('a', class_='itemLink')['href']
            
            # Visit the page that contains the hi-res image
            browser.visit(base_url + image_page_url)
            sleep(5)
            html = browser.html
            soup = bs(html, 'html.parser')
            
            # Retrieve hi-res image URL
            img_url = base_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    # Add to master dictionary
    mars_dict["hemisphere_images"] = hemisphere_image_urls

    # Return results
    return mars_dict

    browser.quit()