#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import pydash as _

import setting

session = requests.Session()

session.cookies.set('access_token', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImE5NzMxNDUzMjcwYjg5YWQzMWFmMTMxZTE4MjFkZWQ1NzRmYTFjYjAzN2UxNDE1NzQ5MDk3Mjk2YmExMDI0ZjI3ZGU0MTJlNTU0NTM0MDhkIn0.eyJhdWQiOiIxIiwianRpIjoiYTk3MzE0NTMyNzBiODlhZDMxYWYxMzFlMTgyMWRlZDU3NGZhMWNiMDM3ZTE0MTU3NDkwOTcyOTZiYTEwMjRmMjdkZTQxMmU1NTQ1MzQwOGQiLCJpYXQiOjE1OTk2MjkxNDgsIm5iZiI6MTU5OTYyOTE0OCwiZXhwIjoxNTk5ODAxOTQ3LCJzdWIiOiI5MjYiLCJzY29wZXMiOltdfQ.MXzeIYXVbhjqWK47i5qCJo0uyrX0MHpzrAbUpHoQeZEfs1hc_QuQVvEFFH2GrEIwhCV27LeUSzDvknqh38lFjm8mBCE3DzzXavncuGdR1Jh1QZX11leRWl8Pbw2BTI1JPypse7Ni-p1oRWFAZConhCs7lsFHscU-zN84lRLGwCHnCpHgIMQ2X9ppFjJE2u8gsE__KDjQ2cOlbJGZzaA87FA-UhsDNLvkGtTpe6O-qtR_xTUI5iHbniDC9Ozn3J1QBVsrpw5jy9uJoNsbhtfPq9lYeLpZGVTkd1o8-KYCN91SmNC1H36UfP-7Y-W1bufOYEN11nFft8tkzTnmuKDEHFoCAppDcCF88n6gQSO0zajZWoiBE2n0iOsWD6cmf9bJtK6FK75tBzSRGfmvUOAp7T8QAjE83IZ3uL7vrQfWaZKdrIq7reXdJC4FXhXP4Qv2jfsnhUwpVMKbG54R7KGcAwc1_P42KkIuziVe_5GBCnZgkM7Tzkpn6hjStfk8tID0YoXE29hvOpaGH9-4mBzvbKF1M4_Nt7ThdlHxzhqXqKLY2I9XWeE4lqL260SeK5zoDPxcTQvTrBHEN7oFg7D6QBMofiLNls_NK9Jz5mlAYOI23oAOi2MYonLEWcZsYIy-tgR8E-8eW3LlJu2S5PiDeAWFjARRiZp43wGFNaEvCcs')
session.cookies.set('refresh_token', 'def502008ef8cda5e4781d109292c93475d9a100c5bfafdd83e5303355ccb5248539ef8b0ca9ede0c739b6b176e6ce2314f97bfca5c97fe339316af98d18cf64c19c55a3668ca7e97d32047bbf73cfa6a9a02a55441a91ce98e1bcbf1e1fc2856c8332fe7b5c415f520c8910ba5925453e323d4834cf4ebb55adbebc4499247ff626b4e1bbd58e4d4403c8b1d66c68cbfab2fa077c5d85673ea45c0144b8f9acf21915808a5e2ccf2c91ae42be7c5b8d3077cb34573b1c7ab4b823529f75380f9afc0b42e01de17b000bccbc2cbc2aca9f39277ec93323412f4090f30e8438d3b30581d8471e5a488fb4c37011321c5ef579b0b2fb33b662ec7c1156ae7b57036b7372cbf2da451d7765ee9ed8d7df9be2f1bc5b95bd4d3e2ce40dcf1a432451c6503015d432ba8cfe8546eaa65a118255023d67602060a8df3705b7af081a5998d9b451af44c64fa418517f2a5dbe1fc37c7d2fe3bcc1840dc0e3b27b00175889df56')
session.cookies.set('XSRF-TOKEN', 'eyJpdiI6Ilg1dXJIQlJcL1NVV2RyaUdwbVNYWmxnPT0iLCJ2YWx1ZSI6ImtwUzNKbWQra1hucU53eUZDOEhVT1RKalJ3YVlsMlRYTnZNZ2dmcFNDdUJhOStuZE5sQ05PZkErSVg3VmMxXC9PIiwibWFjIjoiNzAwODVjNmZkNDI2MjE2Nzc0ODMxNWZlYmI2NmFjZTRlNzczZGIzNWQ4YjgwNDJkNzcyMjBmNWQ2ZGJiOTI4ZSJ9')
session.cookies.set('laravel_session', 'av0m6H15jbtdkclqshs8ahIptNZV6nWQ8hnvn05m')


# link= 'https://goal.sun-asterisk.vn/groups/393'
# response = session.get(link)
# response.encoding = 'utf-8'
# soup = BeautifulSoup(response.content, 'html.parser')
# title = soup.select_one('.breadcrumb-item.active').string

# print(title)

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

# for group in setting.LINKS:
#     print('==========================')
#     print(group)
#     print('==========================')
#     links = setting.LINKS[group]
#     for link in links:
#         response = session.get(link)
#         response.encoding = 'utf-8'
#         soup = BeautifulSoup(response.content, 'html.parser')
#         title = soup.select_one('.breadcrumb-item.active').string
#         print(title)
#         objectives = soup.select('.objectiveItem')
#         for o_idx, objective in enumerate(objectives):
#             objective_name = objective.select_one('.obj-name').get_text()
#             krs = objective.select('.border-left')
#             print("O%s. %s" % (o_idx+1, _.trim(objective_name)))
#             for kr_idx, kr in enumerate(krs):
#                 kr_name = _.trim(kr.select_one('.label-obj').get_text())
#                 kr_desc = _.trim(kr.select_one('.display_enter_char').get_text())
                
#                 if kr_desc:
#                     kr_printout = "KR%s. %s\r\n%s"
#                     print(kr_printout % (kr_idx+1, kr_name, kr_desc))
#                 else:
#                     kr_printout = "KR%s. %s"
#                     print(kr_printout % (kr_idx+1, kr_name))
                
#             print("")
#         print("======")
#         # break