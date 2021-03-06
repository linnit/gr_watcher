#!/usr/bin/env python

from .Bookshop import Bookshop


class Waterstones(Bookshop):
    def __init__(self, author, title):
        super().__init__(author, title)

        self.label = "waterstones"

        self.book_formats = {"Paperback": 17, "Hardback": 16}
        self.bookshop_base_url = "https://www.waterstones.com"
        self.search_url = f"https://www.waterstones.com/books/search/term/{self.search_term}/sort/price-asc"

    def get_book_item(self, soup):
        book_items = soup.findAll(class_="book-preview")

        for book_item in book_items:
            format = book_item.find(class_="format").find(text=True)
            if format != "Cancelled":
                return book_item
