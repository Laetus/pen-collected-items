#!/usr/bin/env python
""" Run preprocessing """
# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient
import classes.Preprocessing as Preprocessing


data_path = str(os.environ['RAW_DATA_PATH'])
data_length = 'long'

if str(os.environ['SHORT_DATA']):
    data_length = 'short'

client = MongoClient(os.environ['DB_URI'])
database = client.get_default_database()
print('database connected')

if not os.getenv('PROCESS_RELATIONS_ONLY', False):
    # process zones
    Preprocessing.zones(data_path + 'zones.csv',  database)

    # process location
    Preprocessing.objects(data_path + 'location-' +
                          data_length + '.csv', database)

# process items
Preprocessing.relations(
    data_path + 'pen-collected-items-' + data_length + '.csv', database)
