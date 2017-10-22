#!/usr/bin/env python
""" Start server """
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
from flask import abort
import classes.Database as Database
import classes.Util as Util

baseUrl = str(os.getenv('BASE_URL', '')) + '/'

app = Flask(__name__)
CORS(app)

db = Database.Database(os.environ['DB_URI'])


@app.route(baseUrl)
def hello():
    return "Hallo Welt"


@app.route(baseUrl + 'field')
def field():
    try:
        location = {
            'x': int(request.args.get('x')),
            'y': int(request.args.get('y'))
        }

        return jsonify(db.handle_single_field(location, request.args))

    except ValueError:
        abort(400)
    except Exception as e:
        print(e)
        abort(500)


@app.route(baseUrl + 'area')
def area():
    try:
        upper_left = {
            'x': int(request.args.get('upper_left_x')),
            'y': int(request.args.get('upper_left_y'))
        }

        bottom_right = {
            'x': int(request.args.get('bottom_right_x')),
            'y': int(request.args.get('bottom_right_y'))
        }

        upper_left_zone = db.get_zone_of_location(
            upper_left, projection={'_id': True, 'id': True})['id']
        bottom_right_zone = db.get_zone_of_location(
            bottom_right, projection={'_id': True, 'id': True})['id']

        print('upper_left_id: ' + str(upper_left_zone))
        print('bottom_right_id: ' + str(bottom_right_zone))

        res = []
        visitor_sum = 0
        object_sum = 0
        for i in Util.getZoneRange(bottom_right_zone, upper_left_zone):

            tmp = db.handle_single_field(i, request.args)
            if tmp is not None:
                res.append(tmp)
                object_sum += tmp['object_count']
                visitor_sum += tmp['visitor_count']

        result = {
            'object_count': object_sum,
            'visitor_sum': visitor_sum,
            'fields': res
        }

        return jsonify(result)

    except ValueError:
        abort(400)
    except Exception as e:
        print(e)
        abort(500)


if __name__ == "__main__":
    app.run()
