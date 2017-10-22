#!/usr/bin/env python
""" Database access """
# -*- coding: utf-8 -*-

import os
import math
from pymongo import MongoClient
import classes.Preprocessing as Preprocessing
import classes.Util as Util
from datetime import date
from datetime import timedelta
# TODO: implement singleton


class Database:
    """ Database access """

    def __init__(self, db_uri):
        self.__db = MongoClient(db_uri).get_default_database()

        self.__zones = self.__db['zones']
        self.__objects = self.__db['objects']
        self.__relations = self.__db['relations']
        self.__visitors_by_day_zone = self.__db['visitors_by_day_zone']

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
        # check validity
        if not isinstance(zone_id, int) and zone_id in range(0, 200):
            raise ValueError

        query = {
            'id': zone_id
        }

        result = self.__zones.find_one(query, projection=projection)
        return result

    def get_visitors_by_day_and_zone(self, zone_id, day, projection={'_id': True, 'id': True, 'visitors': True}):
        # check validity
        if not True:
            raise ValueError

        query = {
            'day': day,
            'zone': zone_id
        }

        result = self.__visitors_by_day_zone.find_one(
            query, projection=projection)
        return result

    def get_object_id(self, object_id):
        return self.__objects.find_one({'refers_to_object_id': object_id}, projection=['_id', 'id', 'zone'])

    def get_visitors_by_time_range_and_zone(self, zone_id, from_date, to_date=date.today()):
        if from_date > to_date:
            raise ValueError

        res_list = []
        max_visitors = -1
        max_date = from_date
        visitor_sum = 0
        act_date = from_date
        while act_date < to_date:
            tmp = self.get_visitors_by_day_and_zone(
                zone_id, Util.date2str(act_date))

            if tmp is not None:
                visitor_count = len(tmp['visitors'])
                visitor_sum += visitor_count
                res_list.append({
                    'visitor_count': visitor_count,
                    'date': Util.date2str(act_date)
                })
                if max_visitors < visitor_count:
                    max_visitors = visitor_count
                    max_date = act_date

            act_date += timedelta(days=1)

        result = {'visitors': res_list,
                  'visitor_count': visitor_sum,
                  'from': Util.date2str(from_date),
                  'to': Util.date2str(to_date)}

        if (max_visitors > 0):
            result['max_visitors'] = {
                'date': Util.date2str(max_date),
                'visitor_count': max_visitors
            }

        return result

    def handle_single_field(self, location, req_args):
        if isinstance(location, dict):
            zone = self.get_zone_of_location(
                location, projection={'_id': True, 'id': True, 'objects': True})
        else:
            zone = self.get_zone(location, projection={
                                 '_id': True, 'id': True, 'objects': True})

        result = {
            'zone_id': zone['id']
        }

        if 'objects' in zone:
            result['object_count'] = len(zone['objects'])

        if 'date' in req_args:
            result['date'] = req_args.get('date')
            tmp = self.get_visitors_by_day_and_zone(
                zone['id'], req_args.get('date'))
            if 'visitors' in tmp:
                result['visitor_count'] = len(tmp['visitors'])
                result['visitors'] = tmp['visitors']

        if 'from' in req_args:
            from_date = Util.str2date(req_args.get('from'))
            if 'to' in req_args:
                to_date = Util.str2date(req_args.get('to'))
            else:
                to_date = date.today()

            result.update(self.get_visitors_by_time_range_and_zone(
                zone['id'], from_date, to_date))

        return result
