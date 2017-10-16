#!/usr/bin/env python
""" Utils """
# -*- coding: utf-8 -*-

import numbers


def inbetween(a, x, b):
    if (a <= b) and isinstance(x, numbers.Number):
        return (a <= x) and (x <= b)
    else:
        raise ValueError
