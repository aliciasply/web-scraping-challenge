#!/usr/bin/env python
# coding: utf-8

# # NASA Mars News
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
# 

# * Step 1 - Scraping

# In[6]:


# Dependencies
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

# In[2]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


# In[3]:


# Retrieve page with the requests module
response = requests.get(url)


# In[4]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')


# In[7]:


# Prettify the code to review the result, then determine element that contains sought info
print(soup.prettify())


# In[8]:


# Examine the block of result, then determine element that contains sought info
results = soup.find_all('div',class_='slide')
# results
results[0]


# In[9]:


# return the title of the news
news_title = soup.find('div', class_='content_title').text
print(news_title)


# In[10]:


# return the paragraph of the news
news_p = soup.find('div', class_='rollover_description_inner').text
print(news_p)        


# # JPL Mars Space Images - Featured Image
# 
# 
# 

# * Visit the url for JPL Featured Space Image here.
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# * Make sure to find the image url to the full size .jpg image.
# * Make sure to save a complete url string for this image.
# 

# In[37]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless=False)


# In[38]:


# URL of the page to be scraped
jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# In[39]:


browser.visit(jpl_image_url)


# In[40]:


html = browser.html
soup = bs(html, "html.parser")


# In[41]:


# The image doesn't have the next button, but it has the FULL Image button
# so we're using the splinter to navigate the site

browser.click_link_by_partial_text("FULL IMAGE")


# In[42]:


# Getting full info of the image from the More Info tab
browser.click_link_by_partial_text("more info")


# In[58]:


results = soup.find_all('figure', class_="lede")

for result in results:
    image = result.a['href']
    featured_image_url = image
# featured_image_url
    print("https://www.jpl.nasa.gov"+ featured_image_url)


# In[59]:


# featured_image_url


# In[60]:


browser.quit()


# # Mars Facts
# 
# 

# 
# * Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# 
# * Use Pandas to convert the data to a HTML table string.

# In[47]:


# URL from Mars Facts webpage
mars_url = 'https://space-facts.com/mars/'


# In[48]:


# Read from URL
mars_table = pd.read_html(mars_url)
mars_table


# In[49]:


len(mars_table)


# In[50]:


mars_df = mars_table[0]
mars_df


# In[52]:


mars_df = mars_table[0]

# Change the columns name
mars_df.columns = ['Description','Value']

# Set the index to the `Description` column 
mars_df.set_index('Description', inplace=True)


# In[53]:


mars_df


# In[54]:


# Save the HTML file
mars_df.to_html('mars_html')


# # Mars Hemispheres

# * Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# 
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[31]:


# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser("chrome", **executable_path, headless=False)


# In[44]:


# Visit hemispheres website through splinter module 
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[45]:


# Retrieve page with the requests module
response = requests.get(hemispheres_url)


# In[46]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, "html.parser")


# In[47]:


# Retreive all items that contain mars hemispheres information
items = soup.find_all('div', class_='item')


# In[62]:


# Create empty list for hemisphere urls 
hemisphere_image_urls = []


# Store to regular url 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
for x in items: 
    # Store title
    title = x.find('h3').text
    
    # Store link that leads to full image website
    partial_img_url = x.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every hemisphere site
    soup = bs( partial_img_html, 'html.parser')
    
    # Extracting the full image 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    print(img_url)
    
    # Append the link and title to the empty link created at the beginning 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    


# In[57]:


# Display hemisphere_image_urls
hemisphere_image_urls


# In[ ]:




