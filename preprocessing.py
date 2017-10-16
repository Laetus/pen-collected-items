#!/usr/bin/env python
""" Run preprocessing """
# -*- coding: utf-8 -*-

import os
import json
from pymongo import MongoClient
import classes.Preprocessing as Preprocessing


material_path = str(os.environ['RAW_DATA_PATH'])
data_length = 'long'

if str(os.environ['SHORT_DATA']):
    data_length = 'short'

client = MongoClient(os.environ['DB_URI'])
database = client.get_default_database()

# process zones
# Preprocessing.zones(material_path + 'zones.csv',  database)

# process location
# Preprocessing.objects(material_path + 'location-' + data_length + '.csv', database)

# process items
#Preprocessing.relations(material_path + 'pen-collected-items-' + data_length + '.csv', database)
