#!/usr/bin/env python
""" Database access """
# -*- coding: utf-8 -*-

import os
import math
from pymongo import MongoClient
import classes.Preprocessing as Preprocessing
import classes.Util as Util


class Database:
    """ Database access """

    def __init__(self, db_uri):
        self.__db = MongoClient(db_uri).get_default_database()

        self.__zones = self.__db['zones']
        self.__objects = self.__db['objects']
        self.__relations = self.__db['relations']

    def get_zone_of_location(self, location, projection={'_id': True, 'id': True}):
        # check validity
        if not Util.inbetween(0, int(location['x']), 200) or not Util.inbetween(0, int(location['y']), 100):
            raise ValueError

        query = {
            'x1': {'$lte': location['x']},
            'x2': {'$gt': location['x']},
            'y1': {'$gt': location['y']},
            'y2': {'$lte': location['y']}
        }

        result = self.__zones.find_one(
            query, projection=projection)
        return result

    def get_zone(self, zone_id, projection={'_id': True, 'id': True, 'objects': True}):
        if not isinstance(zone_id, int) and zone_id in range(0, 200):
            raise ValueError

        query = {
            'id': zone_id
        }

        result = self.__zones.find_one(query, projection=projection)
        return result

    def get_object_id(self, object_id):
        return self.__objects.find_one({'refers_to_object_id': object_id}, projection=['_id', 'id', 'zone'])
