from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # Set up Splinter
    # Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create Mars_dict that we can insert into mongo
    Mars_dict = {}
    # Visit https://redplanetscience.com/
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Get latest article and paragraphb
    news_title=soup.find_all('div', class_='content_title')[0].text
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text 

    # URL of Mars Image to be scraped
    website_image_url='https://spaceimages-mars.com/'
    browser.visit(website_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    obtain_photo = soup.find_all('img')
    choosen_photo = soup.find_all('img')[1]["src"]
    featured_image_url = website_image_url + choosen_photo

    # URL of Mars Table to be scraped
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    type(tables)
    Mars_facts_df = tables[0]
    Mars_facts_df.columns = ["","Mars","Earth"]
    Mars_facts_df = Mars_facts_df.iloc[1:]
    Mars_Table = Mars_facts_df.to_html()
    Mars_Table.replace('\n','')

    # URL of page to be scraped
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    all_angles=soup.find('div', class_='collapsible results')
    hemi_photo_find=all_angles.find_all('div', class_='item')
    hemisphere_image_urls = []

    for item in hemi_photo_find:    
        hemisphere = item.find('div', class_="description")
        title = hemisphere.h3.text
    
        hemi_link = hemisphere.a["href"]
        browser.visit(hemi_url + hemi_link)
    
        jpg_html = browser.html
        jpg_soup = BeautifulSoup(jpg_html, 'html.parser')
    
        jpg_url = jpg_soup.find('li').a['href']

        hemi_dict={
        'title': title,
        'img_url': hemi_url+jpg_url
    }
    
        hemisphere_image_urls.append(hemi_dict)
   

    Mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "Mars_Table": Mars_Table,
        "Hemi_Pics": hemisphere_image_urls

    }

    browser.quit()

    return Mars_dict