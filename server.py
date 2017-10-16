#!/usr/bin/env python
""" Start server """
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
import classes.Database as Database

baseUrl = str(os.getenv('BASE_URL', '')) + '/'

app = Flask(__name__)

db = Database.Database(os.environ['DB_URI'])


@app.route(baseUrl)
def hello():
    return "Hallo Welt"


@app.route(baseUrl + 'field')
def req():
    try:
        location = {
            'x': int(request.args.get('x')),
            'y': int(request.args.get('y'))
        }

        res = db.get_zone_of_location(
            location, projection={'_id': True, 'id': True, 'objects': True})
        result = {
            'field_no': res['id']
        }

        if 'objects' in res:
            result['object_count'] = len(res['objects'])

        return jsonify(result)

    except ValueError:
        abort(400)
    except Exception as e:
        print(e)
        abort(500)


if __name__ == "__main__":
    app.run()
