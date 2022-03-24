#!/usr/bin/env python
# coding: utf-8

# # ManoMano Web Scraping Project
# ### The goal of this project is to scrape the data (of barbecue) that I want to buy from the ManoMano web site. 
# ### Also I would like Python to notify me (send e-mail) when the price of barbecue (98€) drops to a certain value (70€) so that I can pay less for it. :-)

# In[1]:


# Import libraries

from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import pandas as pd
import smtplib


#  

# In[2]:


# Connect to Website and pull in data

item_url = 'https://www.manomano.fr/p/george-foreman-22460-56-george-foreman-barbecue-grille-interieur-exterieur-noir-2000-w-4199630'

item_page = requests.get(item_url)

soup = BeautifulSoup(item_page.content, 'html.parser')

item_title = soup.find('h1').get_text()

all_item_prices = soup.find_all(text='€')
first_item_price = all_item_prices[0].parent.parent
item_price = first_item_price.text

print(item_title)
print(item_price)


#  

# In[3]:


# Clean up the data a little bit

item_price = item_price.replace('€', '.')
item_price


#  

# In[4]:


# Create a timestamp for my output to track when data was collected

today = datetime.date.today()
print(today)


#  

# In[5]:


# Create csv file (write headers and data into the file)

header = ['Title', 'Price', 'Date']
data = [item_title, item_price, today]

with open('ManoManoWebScraperDataset.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)


#  

# In[6]:


#  Create dataframe 

df = pd.read_csv(r'C:\Users\djuki\ManoManoWebScraperDataset.csv')
df


#  

# In[7]:


# Append data to the csv file

with open('ManoManoWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)  


#  

# In[8]:


# I want to try sending myself an email (just for fun) when a price hits below 70€

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login('djukic.vladimir@gmail.com','xxxxxxxx')
    
    subject = "The barbecue you want is below 70€!"
    body = "Hi Vladimir, This is the moment you have been waiting for. Now is your chance to pick up the barbecue of your dreams. Don't mess it up! Link here:https://www.manomano.fr/p/george-foreman-22460-56-george-foreman-barbecue-grille-interieur-exterieur-noir-2000-w-4199630" 
    msg = f"Subject: {subject}\n\n{body}"

    sender = "djukic.vladimir@gmail.com"
    receiver = "djukic.vladimir@gmail.com"
    server.sendmail(sender, receiver, msg.encode('utf-8'))
    


#  

# In[9]:


# Check the price (is below 70€) and send email

def check_price(item_url):

    item_page = requests.get(item_url)

    soup = BeautifulSoup(item_page.content, 'html.parser')

    item_title = soup.find('h1').get_text()

    all_item_prices = soup.find_all(text='€')
    first_item_price = all_item_prices[0].parent.parent
    item_price = first_item_price.text
    item_price = item_price.replace('€', '.')
    item_price
    
    today = datetime.date.today()
    
    header = ['Title', 'Price', 'Date']
    data = [item_title, item_price, today]
    
    with open('ManoManoWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
    print(item_price)
    
    if(float(item_price) < 70.00):
        send_mail()


#  

# In[10]:


# Check the item price

item_url = 'https://www.manomano.fr/p/george-foreman-22460-56-george-foreman-barbecue-grille-interieur-exterieur-noir-2000-w-4199630'
check_price(item_url)


# In[ ]:


# Run check_price after a time set (1800 secondes = 30 min.) and input data into your CSV

while(True):
    item_url = 'https://www.manomano.fr/p/george-foreman-22460-56-george-foreman-barbecue-grille-interieur-exterieur-noir-2000-w-4199630'
    check_price(item_url)
    time.sleep(30*60)


#  

# In[12]:


# Dataframe (CSV file)

df = pd.read_csv(r'C:\Users\djuki\ManoManoWebScraperDataset.csv')
df


# ### Finally, I didn't receive the e-mail because the barbecue price is still 98.64 euros. :-)

#  
