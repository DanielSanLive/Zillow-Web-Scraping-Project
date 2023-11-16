# python3 -m pip install googlesearch-python
# Used to install Python Library to scrap Google

#pip3 install pandas
#Used to install pandas, usefulf or datasets

# pip3 install plotly==5.18.0
#Used to install the plotly 

#import code
from googlesearch import search # get zpid
import pandas as pd
import requests
import json
import io
import plotly.express as px

#Api Key to scrape data through scrapeak, in which a free account was created and used for this project
api_key = "e83cf26e-c1c7-48e5-9032-3ba3298601b9"


# useful settings for data display
pd.set_option('display.max_columns', None)
     
#FUNCTIONS for Scraping Zillow Information Data
def get_listings(api_key, listing_url):
    url = "https://app.scrapeak.com/v1/scrapers/zillow/listing"

    querystring = {
        "api_key": api_key,
        "url": listing_url
    }

    return requests.request("GET", url, params=querystring)

def get_property_detail(api_key, zpid):
    url = "https://app.scrapeak.com/v1/scrapers/zillow/property"

    querystring = {
        "api_key": api_key,
        "zpid": zpid
        }

    return requests.request("GET", url, params=querystring)

def get_zpid(api_key, street, city, state, zip_code=None):
    url = "https://app.scrapeak.com/v1/scrapers/zillow/zpidByAddress"

    querystring = {
        "api_key": api_key,
        "street": street,
        "city": city,
        "state": state,
        "zip_code": zip_code
    }

    return requests.request("GET", url, params=querystring)

#Zillow search via url
rent_listing_url = "https://www.zillow.com/seattle-wa/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.74648362207031%2C%22east%22%3A-121.94310837792969%2C%22south%22%3A47.43140094945084%2C%22north%22%3A47.7943069502502%7D%2C%22usersSearchTerm%22%3A%22Seattle%2C%20WA%22%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A16037%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22min%22%3A1000%2C%22max%22%3A2400%7D%2C%22price%22%3A%7B%22min%22%3A181717%2C%22max%22%3A436121%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"

#acquire the listings
rent_listing_response = get_listings(api_key, rent_listing_url)

#to view all keys
print(rent_listing_response.json().keys())

#check if the request was succesful
print("Request success:", rent_listing_response.json()["is_success"])

#view the available count of properties in returned request
num_of_properties = rent_listing_response.json()["data"]["categoryTotals"]["cat1"]["totalResultCount"]
print("Count of properties:", num_of_properties)

#view all the listings
df_rent_listings = pd.json_normalize(rent_listing_response.json()["data"]["cat1"]["searchResults"]["mapResults"])
print("Number of rows:", len(df_rent_listings))
print("Number of columns:", len(df_rent_listings.columns))
df_rent_listings

#view the prices
px.box(df_rent_listings, x="hdpData.homeInfo.price", title="Rental Price Box Plot")

#view the rental zestimate(zillows estimate value of the property)
px.box(df_rent_listings, x="hdpData.homeInfo.rentZestimate", title="Rent Zestimate Box Plot")

#to download the data to view in Excel or related software
df_rent_listings.to_csv('rental_listings_2bed_output.csv', index=False)

