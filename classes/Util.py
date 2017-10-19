#!/usr/bin/env python
""" Utils """
# -*- coding: utf-8 -*-

import numbers
from datetime import date
from datetime import datetime


def inbetween(a, x, b):
    if (a <= b) and isinstance(x, numbers.Number):
        return (a <= x) and (x <= b)
    else:
        raise ValueError


def str2date(datestring):
    try:
        return datetime.strptime(datestring, '%Y-%m-%d').date()
    except:
        raise ValueError


def date2str(datum):
    return datum.strftime('%Y-%m-%d')
