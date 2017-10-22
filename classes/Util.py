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
