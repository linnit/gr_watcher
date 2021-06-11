#!/usr/bin/env python


from bs4 import BeautifulSoup
import logging
import requests
import urllib
from unidecode import unidecode
import re


class Bookshop:
    def __init__(self, author, title):
        self.book_format = None

        self.search_url = ""

        self.author = author
        self.title = title
        self.price = ""

        self.bookshop_base_url = ""
        self.search_url = ""
        self.search_term = urllib.parse.quote_plus(
            unidecode(f"{self.author} {self.title}")
        )

    def set_format(self, format="Paperback"):
        self.book_format = self.book_formats[format]

    def clean_price(self):
        price_regexp = re.compile("\d+\.\d+")
        cleaned_price = price_regexp.search(self.price)
        if cleaned_price:
            self.price = cleaned_price.group()
        else:
            self.price = "0.00"

    def get_price_text(self, book_item):
        return book_item.find(class_="price").find(text=True)

    def get_book_url(self, book_item):
        return book_item.find(class_="title").get("href")

    def get_price(self):
        r = requests.get(self.search_url)

        soup = BeautifulSoup(r.content, "html.parser")

        if r.history:
            self.handle_redirect(soup, r)
            return

        book_item = self.get_book_item(soup)

        if book_item:
            self.price = self.get_price_text(book_item)
            self.clean_price()
            href = self.get_book_url(book_item)

            self.book_url = f"{self.bookshop_base_url}{href}"
        else:
            logging.error(
                f"No price found for {self.author} {self.title} - {self.search_url}"
            )