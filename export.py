#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import pydash as _

import setting

session = requests.Session()
session.cookies.set('access_token', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjA5MmM5ZmQxYjZkMGM1ZjNhMGJmMDMxMTEyNmFjMzY2ZTJkMTU0YWYwYWIzYjk4Y2ZkMjI1ZWVkZTY5ZjljZDBlM2RjN2IzY2MwMzM4NjNhIn0.eyJhdWQiOiIxIiwianRpIjoiMDkyYzlmZDFiNmQwYzVmM2EwYmYwMzExMTI2YWMzNjZlMmQxNTRhZjBhYjNiOThjZmQyMjVlZWRlNjlmOWNkMGUzZGM3YjNjYzAzMzg2M2EiLCJpYXQiOjE1OTk0NDc0NTYsIm5iZiI6MTU5OTQ0NzQ1NiwiZXhwIjoxNTk5NjIwMjU2LCJzdWIiOiI5MjYiLCJzY29wZXMiOltdfQ.HYFZiTFYxldizs1EcwOvI9SiVA0R2iINlqgGzAQUYGUb-0RK11LJANRMEI865nRfm96G6vUVZFnu0SLkFkay6AHJSCBTUheCj9CEyn9hgVKWpCV1QaAV0T4K02Ju3kx--neE6L2RhQIP4BQETorjpkJDeDv2WHRqVummxvMj8Re14Xuy048gcCJd-kmtOL5PX53lWgy-wmWve8n2OX5B8_73gGxsEaQtCx48QEspfsVloUxr3sR9J81Jzen_SfONYvxlPBuh55289gdQ-UN0HhskJgLv4mqYRhpIqqiu7negtzpN1jp2sDK6ABpySwm3WCUrh0OivKWtS5nT-MFqTNYbIYMma3IpZK1sA18rP0VSmzdKUEm1HbwtypFdeWm9FpHVIWk0UJqw1Jpp0GX4-3XJwLnbtdkHYwA8el04SPD7m_5ZEiUny42mz993CUPOVYkWiS8Tvx_o075oXPXam6s8FiGPrs6E6fwuo8ofwzO7BIlly1DCOSHAWHqUUI89V1e2jCuO4FS0L3dHv0DJl4VNuyAo5qvR_fIeh3XXDkwMPH9iIg2rB8EgrjXpPONE2Ke3jhyDU4cRhZGKPGhbbLtSc_22c_td0ZX4iKpF_b22P3ZRwaTcsyURwFgWpjiC3kgnR7yhBeeVc4WSh4L6YBKfgy3Src_LZwuRwbA5_8E')
session.cookies.set('refresh_token', 'def5020096a340a013291c4abdbfcf61fc47b547da8a6803116c28642420e5d3b0f192d8ab1b13e53ebf7ee7846dd638aaa0a39d7d887c6cb4cc7310b6707e6329786d73604fd708a2da567853d73f12dfcc305dfe39d5e26de9082d80261a4c17f8de76421fbc1730441e73579d3416b1273b51165af277cb4abac3d86663cad1d04de1fa7a70b7090996a1d1f58cc6027425a62a3dab74c4b255c827daa294978ff045f344eb14d8cc32050354c8a15084d71bb5dff9a115cab8424ab9a8b63a359b7f423bc2de951a03877cf905d67393962034da36c24c46d9a2c9dff88f77411d1f98f4a35eb905eaa7c3ab51fb37f916d53829d95a21b82c76329ab7c34956d2ed63424d3566f3a44bd1689c681f1d82fd1fccd164299c03d8d0d0652aafbef170ee7cb8595e550b3bcfaf5301495d37f3a4ba87a563539fe568fc6e29160276808ef56e9bf0c598a0db2c621a3083256f8e5555061051798ad5ecbb59320470')
session.cookies.set('XSRF-TOKEN', 'eyJpdiI6IkxOWW5uVzE5bDJQZnNJQkMrVEdDVnc9PSIsInZhbHVlIjoiYzF1MjRTb1hMTVRQK2FMcTNLSjJOYkNcL3hFU2lKMEZab0dKSXJLWWhoOGo2Tm9jXC9zWmhGdzQwbzBMN3hcL1BFMSIsIm1hYyI6IjUzZDIxMTQ3YWI5NDViNmJkNGRkNGUxZGVjMzhjMDVjZTBjZGYwYjdiMDM3NmZhZDEyNDdmN2E4NjFkNzAxNTYifQ%3D%3D')
session.cookies.set('laravel_session', 'MtgdcBRFPv0buHxCDIKDcH6y7OgnrV8cskVhjWDv')


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