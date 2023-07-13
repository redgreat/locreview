#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author by wangcw 
# @generate at 2023/7/12 09:36

from flask import Flask, render_template, request, jsonify
from utils.db import po_google
from utils.geoswitcher import wgs84_to_gcj02
import yaml
import os

pwd = os.getcwd()
config_path = os.path.join(pwd, '../config/config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    conf = yaml.safe_load(f.read())
js_api_key = conf['PRODUCTION']['JSAPI_KEY']
js_api_sec = conf['PRODUCTION']['JSAPI_SEC']

app = Flask(__name__, template_folder='../templates')

def getdevice():
    try:
        con_google = po_google.get_connection()
        cur_google = con_google.cursor(dictionary=True)
        sql_deviceid = 'SELECT DISTINCT device_id FROM carlocdaily;'
        cur_google.execute(sql_deviceid)
        result = cur_google.fetchall()
        devices = []
        for i in result:
            devices.append(i.get('device_id'))
    except Exception as e:
        result = dict(error=str(e))
        return jsonify(result)
    finally:
        cur_google.close()
        con_google.close()
    return devices


@app.route('/')
def index():
    devices = getdevice()
    return render_template('index.html', devices=devices, js_api_key=js_api_key, js_api_sec=js_api_sec)


@app.route('/api/locations')
def locations():
    device_id = request.args.get('device_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    try:
        con_google = po_google.get_connection()
        cur_google = con_google.cursor(dictionary=True)
        sql_locations = 'SELECT lng, lat ' \
                        'FROM carlocdaily WHERE device_id = %s AND dev_upload >= %s AND dev_upload < %s ' \
                        'ORDER BY dev_upload;'
        params = [device_id, start_time, end_time]
        cur_google.execute(sql_locations, params)
        result = cur_google.fetchall()
        array = []
        for row in result:
            gcj02 = wgs84_to_gcj02(float(row.get('lng')), float(row.get('lat')))
            array.append(gcj02)
    except Exception as e:
        result = dict(error=str(e))
        return jsonify(result)
    finally:
        cur_google.close()
        con_google.close()
    return array


if __name__ == '__main__':
    app.run(debug=True)
