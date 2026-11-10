#
#
#
# New scraper for -> Hubgets
# Hubgets page -> https://www.hubgets.com/jobs/

#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
from _county import get_county, translate_city


JOBS_URL = 'https://www.hubgets.com/jobs/'

WAYBACK_CDX = 'https://web.archive.org/cdx/search/cdx'
WAYBACK_BASE = 'https://web.archive.org/web/'


def fetch_jobs_html():
    """
    ... get the Hubgets jobs page HTML. The live page rejects
    datacenter traffic with 403, so fall back to the newest
    Wayback Machine snapshot of the same page.
    """

    try:
        response = requests.get(JOBS_URL, headers=DEFAULT_HEADERS,
                                timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return fetch_jobs_html_from_wayback()


def fetch_jobs_html_from_wayback():
    """
    ... newest archived copy (status 200) of the jobs page.
    """

    cdx_params = {
        'url': JOBS_URL,
        'output': 'json',
        'limit': -1,
        'fl': 'timestamp',
        'filter': 'statuscode:200',
    }
    cdx_response = requests.get(WAYBACK_CDX, params=cdx_params,
                                headers=DEFAULT_HEADERS, timeout=30)
    cdx_response.raise_for_status()
    rows = cdx_response.json()
    if len(rows) < 2:
        return ''
    timestamp = rows[1][0]
    wayback_url = f'{WAYBACK_BASE}{timestamp}if_/{JOBS_URL}'
    response = requests.get(wayback_url, headers=DEFAULT_HEADERS,
                            timeout=60)
    response.raise_for_status()
    return response.text


def req_and_collect_data_():
    """
    ... this func() make a simple requests
    and collect data from Hubgets jobs page.
    """

    soup = BeautifulSoup(fetch_jobs_html(), 'lxml')

    soup_data = soup.find_all('tr')

    lst_with_data = []

    for dt in soup_data:
        title = dt.find('h2')
        location = dt.find('h3', class_="pull-right")
        link = dt.find('div', class_='row clickable')
        if title:
            city = translate_city(location.text.split('/')[1].strip())
            county = get_county(city)
            lst_with_data.append({
                "job_title": title.text,
                "job_link": 'https://www.hubgets.com/jobs/#job-' + link['data-job-id'],
                "company": "Hubgets",
                "country": "Romania",
                "city": city,
                "county": county
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Hubgets'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Hubgets',
                  'https://www.hubgets.com/media/images/logo-hubgets-simple@2x.png'
                  ))
