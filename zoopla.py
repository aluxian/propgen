from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlunparse
import json
import os
import requests
import sys


def price(listing):
    price_node = listing.find('a', class_='text-price')
    try:
        price = list(price_node.children)[2]
    except:
        price = price_node.get_text()

    price = (
        price
            .strip()
            .replace(',', '')
            .replace(u'\xa3', '')
    )

    try:
        return int(price)
    except:
        return None


def beds(listing):
    try:
        return int(
            listing
                .find('span', class_='num-beds')
                .get_text()
                .strip()
        )
    except:
        return None


def parse_listing(listing):
    return {
        'listing_id': int(listing.attrs['data-listing-id']),
        'price': price(listing),
        'latitude': listing
            .find('meta', itemprop='latitude')
            .attrs['content'],
        'longitude': listing
            .find('meta', itemprop='longitude')
            .attrs['content'],
        'beds': beds(listing)
    }


def parse_listings(listings):
    return map(parse_listing, listings)


params = {
    'q': 'london',
    'results_sort': 'newest_listings',
    'search_source': 'home',
    'price_frequency': 'per_month',
    'radius': 0,
    'identifier': 'london',
    'page_size': 100,
    'pn': 1
}

url = urlunparse([
    'http',
    'www.zoopla.co.uk',
    'to-rent/property/london/',
    '',
    urlencode(params),
    ''
])

soup = BeautifulSoup(requests.get(url).content, 'html5lib')

print(len(soup.find_all('li', attrs={'data-listing-id': True})))

#listings = parse_listings()

# list(map(json.dumps, listings))
