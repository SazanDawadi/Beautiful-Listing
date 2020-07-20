import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

base_craig_url = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# view for your base(home) page.
def base(request):
    context = {}
    return render(request , 'my_app/main.html',context)


# view for search result page
def new_search(request):

    # search is equal the keyword you searched on form
    search = request.POST.get('search')
    scrap_url = base_craig_url.format(quote_plus(search))
    response = requests.get(scrap_url)
    data = response.text
    soup = BeautifulSoup(data,features='html.parser')
    # post_list is the list of all the craig post fot the keyword you typed
    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = []

    for post in post_listings:
        # post title holds titles of the posts
        post_title = post.find(class_='result-title').text
        # post_url holds URL of that post
        post_url = post.find('a').get('href')

        # litl_txt holds the small line of text that appears after post title in craiglist post
        if post.find(class_='result-hood'):
            litl_txt = post.find(class_='result-hood').text
        else:
            litl_txt = '' 
        

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        # post_price holds the price of that craig post and it will be set as N/A if price is not available
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
           
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
         # post_image_url is set to default craiglist image url if no image is available

        final_postings.append((post_title, post_url, post_price, post_image_url,litl_txt))


    context = {
        'search':search,
        'final_postings':final_postings,
        }
    return render(request,'my_app/home.html',context)