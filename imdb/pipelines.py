# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import sqlite3

# class ImdbPipeline(object):
#     def process_item(self, item, spider):
#         return item

class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    title TEXT,
                    year TEXT,
                    genre TEXT,
                    rating TEXT,
                    duration TEXT,                
                    movie_url TEXT
                )
            
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()


    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies (title,year,genre,rating,duration,movie_url) VALUES(?,?,?,?,?,?)

        ''', (
            item.get('title'),
            item.get('year'),
            item.get('genre'),
            item.get('rating'),
            item.get('duration'),  
            item.get('movie_url')
        ))
        self.connection.commit()
        return item