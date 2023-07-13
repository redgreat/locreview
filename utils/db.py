#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author by wangcw 
# @generate at 2023/7/12 09:46

from mysql.connector.pooling import MySQLConnectionPool
import yaml
import os

pwd = os.getcwd()
config_path = os.path.join(pwd, '../config/config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    conf = yaml.safe_load(f.read())

conf_db = conf['PRODUCTION']['DATABASES']
ti_google = conf_db.get('TI_GOOGLE')
ti_msn = conf_db.get('TI_MSN')

po_google = MySQLConnectionPool(host=ti_google['host'],
                                user=ti_google['user'],
                                password=ti_google['password'],
                                db=ti_google['database'],
                                port=ti_google['port'],
                                ssl_ca=ti_google['ssl_ca'],
                                ssl_cert=None,
                                ssl_key=None,
                                charset='utf8mb4',
                                pool_name='po_src',
                                pool_size=5,
                                time_zone='+8:00')

po_msn = MySQLConnectionPool(host=ti_msn['host'],
                             user=ti_msn['user'],
                             password=ti_msn['password'],
                             db=ti_msn['database'],
                             port=ti_msn['port'],
                             ssl_ca=ti_msn['ssl_ca'],
                             ssl_cert=None,
                             ssl_key=None,
                             charset='utf8mb4',
                             pool_name='po_src',
                             pool_size=5,
                             time_zone='+8:00')
