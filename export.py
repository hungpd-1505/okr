#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import pydash as _

import os
from dotenv import load_dotenv

load_dotenv(override=True)

session = requests.Session()

session.cookies.set('access_token', os.getenv('access_token'))
session.cookies.set('refresh_token', os.getenv('refresh_token'))
session.cookies.set('XSRF-TOKEN', os.getenv('xsrf_token'))
session.cookies.set('laravel_session', os.getenv('laravel_session'))

def group_data(group_id):

    response = session.get('https://goal.sun-asterisk.vn/groups/%d' % group_id)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')
    title = '-'
    try:
        title = soup.select_one('.breadcrumb-item.active').string
    except:
        pass
    output = {
        "name": title,
        "objectives": []
    }
    # print(title)
    objectives = soup.select('.objectiveItem')
    if objectives:
        for o_idx, objective in enumerate(objectives):
            objective_name = _.trim(objective.select_one('.obj-name').get_text())
            objective_percent = _.trim(objective.select_one('.keep-break').get_text())
            krs = objective.select('.border-left')
            
            objective_json = {
                "name": _.trim(objective_name),
                "progress": objective_percent,
                "krs": []
            }
            # print("O%s. %s" % (o_idx+1, _.trim(objective_name)))
            if krs:
                for kr_idx, kr in enumerate(krs):
                    kr_name = _.trim(kr.select_one('.label-obj').get_text())
                    kr_desc = _.trim(kr.select_one('.display_enter_char').get_text())
                    kr_percent = _.trim(kr.select_one('.keep-break').get_text())

                    target_unit = '-'
                    target_progress = '-'

                    try:
                        target = objective.select('.modal')[kr_idx]

                        target_unit = target.select_one('.targetunit').attrs['title']
                        target_progress = target.select_one('.keyResultSliderDetailInput').attrs['value']

                    except:
                        pass

                    kr_json = {
                        "name": kr_name,
                        "desc": kr_desc,
                        "progress": kr_percent,
                        "target": "%s/%s" % (target_progress, target_unit),
                    }
                    objective_json['krs'].append(kr_json)
            output['objectives'].append(objective_json)

            # print("")
        # print("======")
    return output


def refresh_token():
    """
    refresh token
    execute each 3 hours
    """
    session.get('https://goal.sun-asterisk.vn/groups/1225')
    print('refresh token successfuly!')