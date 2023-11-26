#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pb
import cv2
from bs4 import BeautifulSoup


# In[5]:


import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[47]:


website_url="https://www.makemytrip.com/flights/airlines.html"


# In[53]:


driver = webdriver.Chrome()
driver.get(website_url)

driver.maximize_window()

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

resolution = [1920, 870]
script = f"return [window.screen.width = {resolution[0]}, window.screen.height = {resolution[1]}];"
original_screen_resolution = driver.execute_script(script)


photo = driver.get_screenshot_as_png()

photo_np = cv2.imdecode(np.frombuffer(photo, np.uint8), 1)

page = cv2.cvtColor(photo_np, cv2.COLOR_BGR2RGB)


for tag in driver.find_elements(By.CSS_SELECTOR, 'div:not(:empty):not(:has(*)),img,li,label,a,button,h1,h2,h3,input,span:not(:empty):not(:has(*))'):
    try:
        location = tag.location
        size = tag.size
        x, y = location['x'], location['y']
        x_max, y_max = x + size['width'], y + size['height']
        margin_x = int(size['width'] * 0.1) 
        margin_y = int(size['height'] * 0.1) 

        x -= margin_x
        y -= margin_y
        x_max += margin_x
        y_max += margin_y

        x = int(x * original_screen_resolution[0] / driver.execute_script("return window.innerWidth;"))
        y = int(y * original_screen_resolution[1] / driver.execute_script("return window.innerHeight;"))
        x_max = int(x_max * original_screen_resolution[0] / driver.execute_script("return window.innerWidth;"))
        y_max = int(y_max * original_screen_resolution[1] / driver.execute_script("return window.innerHeight;"))

      


        cv2.rectangle(webpage_rgb, (x, y), (x_max, y_max), (0, 185, 255), 2)
    except AttributeError:
        pass  
def get_website_details(links):
    
    try:
        driver.get(links)

        driver.implicitly_wait(5)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.text
        meta_description = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else None
        print(f"Title: {title}")
        print(f"Meta Description: {meta_description}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

get_website_details(website_url)

    
    
cv2.namedWindow('Webpage with Boundaries', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Webpage with Boundaries', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
cv2.imshow('Webpage with Boundaries', webpage_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()

driver.quit() 


# In[ ]:





# In[ ]:




