# -*- coding: utf-8 -*-

import pymongo
import os

class MongoPipeline(object):

    collection_name = 'snowReports'

    def __init__(self):
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        db = client.skiResorts
        self.collection = db[self.collection_name]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item



class TrialCrawlsPipeline(object):
    def process_item(self, item, spider):
        return item
