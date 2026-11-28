#
#
#
# New scraper for -> PixelBowlStudio
# PixelBowlStudio page -> https://pixelbowlstudio.com/careers/
# (old /job-opening/ page redirects to /careers/)
# Jobs are listed in the "open positions" accordion on the careers page.

#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#

import re
import requests
from bs4 import BeautifulSoup
#

CAREERS_URL = 'https://pixelbowlstudio.com/careers/'


def _js_add(left, right):
    if isinstance(left, str) or isinstance(right, str):
        return str(left) + str(right)
    return left + right


def _decode_challenge_number(expr):
    values = {'+!+[]': 1, '+![]': 0, '!![]': 1, '[]': ''}
    result = 0
    for group in re.findall(r'\(([^()]+)\)', expr):
        value = 0
        for token in re.findall(r'\+!\+\[\]|\+!\[\]|!!\[\]|\[\]', group):
            value = _js_add(value, values[token])
        result = _js_add(result, value)
    return int(result)


def _get_page_soup_(session):
    response = session.get(CAREERS_URL, headers=DEFAULT_HEADERS)
    if 'One moment, please...' not in response.text:
        return BeautifulSoup(response.text, 'lxml')

    html = response.text
    first_expr = html[html.index('A=+') + 2:html.index(',u=window')]
    second_expr = html[html.index('i=+') + 2:html.index(",b='wsidchk'")]
    path = re.search(r"y='([^']+)'", html).group(1)
    timestamp = re.search(r"ts','(\d+)'", html).group(1)
    pdata = re.search(r"H='([^']+)'", html).group(1)

    params = {
        'wsidchk': _decode_challenge_number(first_expr) + _decode_challenge_number(second_expr),
        'pdata': pdata,
        'id': '7fa3b767c460b54a2be4d49030b349c7',
        'ts': timestamp,
        'cttl': '0'
    }
    session.get('https://pixelbowlstudio.com' + path,
                params=params,
                headers={**DEFAULT_HEADERS, 'Referer': CAREERS_URL})

    response = session.get(CAREERS_URL, headers=DEFAULT_HEADERS)
    return BeautifulSoup(response.text, 'lxml')


def req_and_collect_data_():
    """
    ... this func() makes simple requests
    and collects data from PixelBowlStudio job pages.
    """

    page_soup = _get_page_soup_(requests.Session())

    open_positions = page_soup.find(id='open-positions')
    if not open_positions:
        return []

    lst_with_data = []

    for item in open_positions.find_all('div', class_='accordion-item'):
        title = item.find('button', class_='accordion-button')
        if not title:
            continue

        header = item.find('h2', class_='accordion-header')
        anchor = header.get('id') if header else None
        job_link = f"{CAREERS_URL}#{anchor}" if anchor else CAREERS_URL

        lst_with_data.append({
            "job_title": title.get_text(strip=True),
            "job_link": job_link,
            "company": "PixelBowlStudio",
            "country": "Romania",
            "city": "Bucuresti",
            "county": "Bucuresti"
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'PixelBowlStudio'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('PixelBowlStudio',
                  'https://pixelbowlstudio.com/wp-content/uploads/2022/11/logo1-1536x331.jpg'
                  ))
