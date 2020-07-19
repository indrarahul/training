from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import action
from rq import Queue
import pickle
from redis import Redis
from bs4 import BeautifulSoup
import requests

redisClient = Redis(host='redis')
bookInfoParserQueue = Queue('bookInfoParser',connection=redisClient)
generate_redis_key_for_book = lambda bookURL: 'GOODREADS_BOOKS_INFO:' + bookURL

def parse_book_link_for_meta_data(bookLink):
  htmlString = requests.get(bookLink).content # Fetch HTML string of the book information page
  bsTree = BeautifulSoup(htmlString,"html.parser") # Build a searchable tree using fetched HTML
  # Find the required book attributes in the tree
  title = bsTree.find("h1", attrs={"id": "bookTitle"}).string
  author = bsTree.find("a", attrs={"class": "authorName"}).span.string
  rating = bsTree.find("span", attrs={"itemprop": "ratingValue"}).string
  description = ''.join(bsTree.find("div", attrs={"id": "description"}).find("span", attrs={"style": "display:none"}).stripped_strings)
  return dict(title=title.strip() if title else '',author=author.strip() if author else '',rating=float(rating.strip() if rating else 0),description=description)

def parse_and_persist_book_info(bookUrl):
  redisKey = generate_redis_key_for_book(bookUrl)
  bookInfo  = parse_book_link_for_meta_data(bookUrl) 
  redisClient.set(redisKey,pickle.dumps(bookInfo))
  
def parse_goodreads_urls(request):
  bodyJSON = request.get_json() # Get JSON body from POST request
  if (isinstance(bodyJSON,list) and len(bodyJSON)): # Check whether JSON is list or not
    bookLinksArray = [x for x in list(set(bodyJSON)) if x.startswith('https://www.goodreads.com/book/show/')] #validation check for goodreads book URL
    if (len(bookLinksArray)):
      for bookUrl in bookLinksArray:
        bookInfoParserQueue.enqueue_call(func=parse_and_persist_book_info,args=(bookUrl,),job_id=bookUrl) # enqueue to Redis queue
      return "%d books are scheduled for info parsing."%(len(bookLinksArray))
  return "Only array of goodreads book links is accepted.",400