#!/usr/bin/env python
# coding: utf-8

# In[13]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[14]:


# Path to chromedriver
#!which chromedriver


# In[39]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[17]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[18]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[19]:


slide_elem.find("div", class_='content_title')


# In[20]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[21]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[22]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[23]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[24]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[25]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[26]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[27]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[28]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[29]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[30]:


df.to_html()


# ### Mars Weather

# In[31]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[32]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[33]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[41]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[48]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in range (0, 4):
    html1 = browser.html
    quote_soup = soup (html1, 'html.parser')
    titles = quote_soup.find_all('h3')
    title=titles[x].text
    browser.links.find_by_partial_text(title).click()
    
    html2 = browser.html
    mars_image= soup (html2, 'html.parser')
    mars_url = mars_image.select_one("div.downloads a").get("href")
    
    
    hemispheres ={"img_url":mars_url,"title":title}
    hemisphere_image_urls.append(hemispheres)
    
    browser.visit(url)


# In[49]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[50]:


# 5. Quit the browser
browser.quit()


# In[ ]:




