#!/usr/bin/env python
""" Methods for preprocessing """
# -*- coding: utf-8 -*-

import csv
import time
from datetime import datetime


def zones(path, database):
    zones = database['zones']
    zones.remove({})

    reader = csv.DictReader(open(path, 'r'), quotechar='"')
    count = 0
    for row in reader:
        count += 1
        process_zone(row, zones)

    assert count is 200


def process_zone(row, collection):
    for item in row:
        row[item] = int(row[item])
    row['objects'] = []
    collection.insert_one(row)


def objects(path, database):
    objects = database['objects']
    objects.remove({})

    reader = csv.DictReader(open(path, 'r'), quotechar='"')
    count = 0
    for row in reader:
        count += 1
        process_object(row, objects, database['zones'])

    print(count)


def process_object(row, collection, zones):
    for item in row:
        if 'id' not in item:
            row[item] = float(row[item])
        else:
            row[item] = int(row[item])

    row['zone'] = get_zone(zones, row)
    object_id = collection.insert_one(row).inserted_id
    update = {
        '$push': {'objects': object_id}
    }
    zones.find_one_and_update({'id': row['zone']}, update)


@DeprecationWarning
def get_zone(zones, row):
    query = {
        'x1': {'$lte': row['x']},
        'x2': {'$gt': row['x']},
        'y1': {'$gt': row['y']},
        'y2': {'$lte': row['y']}
    }

    result = zones.find_one(query, projection={'_id': True, 'id': True})
    return result['id']


def relations(path, database):
    relations = database['relations']
    relations.remove({})
    visitors_by_day_zone = database['visitors_by_day_zone']
    visitors_by_day_zone.remove({})

    reader = csv.DictReader(open(path, 'r'), quotechar='"')
    count = 0
    start = time.time()
    for row in reader:
        count += 1
        process_relation(row, relations, database)
        if count % int(1e3) is 0:
            print(count)
        if count > 4e4:
            break

    end = time.time()
    print(end - start)
    print(count)


def process_relation(row, collection, database):
    for item in row:
        if 'bundle_id' not in item:
            row[item] = int(row[item])
    object_element = get_object_id(row['refers_to_object_id'], database)
    zone = object_element['zone']
    day = datetime.fromtimestamp(row['created']).strftime('%Y-%m-%d')
    query = {
        'day': day,
        'zone': zone
    }
    update = {
        '$push': {'visitors': row['bundle_id']}
    }
    collection.insert_one(row)
    database['visitors_by_day_zone'].find_one_and_update(query, update)


@DeprecationWarning
def get_object_id(object_id, database):
    return database['objects'].find_one({'refers_to_object_id': object_id}, projection=['_id', 'id', 'zone'])