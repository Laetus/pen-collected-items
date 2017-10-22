#!/usr/bin/env python
""" Utils """
# -*- coding: utf-8 -*-

import numbers
from datetime import date
from datetime import datetime

length_x = 20


def inbetween(a, x, b):
    if (a <= b) and isinstance(x, numbers.Number):
        return (a <= x) and (x <= b)
    else:
        raise ValueError


def getZoneRange(zone1_id, zone2_id):
    edges = [zone1_id, zone2_id]
    modulo = list(map(lambda x: int(x % length_x), edges))
    multiple = list(map(lambda x: int(x // length_x), edges))
    res = []
    for i in range(min(multiple), max(multiple) + 1):
        res += list(range(min(modulo) + i * length_x,
                          (max(modulo) + 1) + i * length_x))
    return res


def str2date(datestring):
    try:
        return datetime.strptime(datestring, '%Y-%m-%d').date()
    except:
        raise ValueError


def date2str(datum):
    return datum.strftime('%Y-%m-%d')


def params2query(zone_id, req_args):
    reqarg = {}
    for key in req_args.keys():
        if key not in set(['upper_left_x', 'upper_left_y', 'bottom_right_x', 'bottom_right_y', 'x', 'y']):
            reqarg[key] = req_args[key]

    return {
        'zone_id':  zone_id,
        'request-args': reqarg
    }
