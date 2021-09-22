from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # Set up Splinter
    # @NOTE: Replace the path with your actual path to the chromedriver
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
    featured_image_url='https://spaceimages-mars.com/image/featured/mars3.jpg'
    browser.visit(featured_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # URL of Mars Table to be scraped
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    type(tables)
    Mars_facts_df = tables[0]
    Mars_facts_df.head()
    Mars_Table = Mars_facts_df.to_html()
    Mars_Table.replace('\n','')

    Mars_dict = {
        "News_Title": news_title,
        "News_p": newsp
    }

    browser.quit()

    return Mars_dict