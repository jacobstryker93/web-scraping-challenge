from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser("chrome",**executable_path, headless=False)

def scrape(browser):
    final_data = {}
    output = marsNews(browser)
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data


def marsNews(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    browser.is_element_present_by_css('.slide', wait_time=1)
    soup = BeautifulSoup(html, "html.parser")
    news_title_trial = soup.select(".slide .content_title a")
    news_title = news_title_trial[0].get_text()
    paragraph_trial = soup.select(".slide .article_teaser_body")
    paragraph = paragraph_trial[0].get_text()
    output = [news_title, paragraph]
    return output


def marsImage(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    photo_trial2 = browser.find_by_id('full_image')
    photo_trial2.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    photo_trial3 = browser.links.find_by_partial_text('more info')
    photo_trial3.click()
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    image_url = image_soup.find("figure", class_="lede")
    image_url2 = image_url.find("img")["src"]
    featured_image_url = f'https://www.jpl.nasa.gov{image_url2}'
    return featured_image_url


def marsFacts(browser):
    import pandas as pd
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars = pd.read_html(facts_url)
    mars_df = pd.DataFrame(mars[0])
    mars_info = mars_df.to_html(header=False, index=False)
    return mars_info

def marsHem(browser):
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemisphere_mars_final = []
    results = soup.find("div", class_="result-list")
    hemispheres = results.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace(" Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_mars_final.append({"title": title, "img_url": image_url})
        return hemisphere_mars_final