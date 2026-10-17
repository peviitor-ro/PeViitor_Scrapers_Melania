#
#
#
# New scraper for -> Druid
# Druid page -> https://www.druidai.com/careers

#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
from _county import get_county, translate_city


def req_and_collect_data_():
    """
    ... this func() make a simple requests
    and collect data from Druid careers page.
    """

    response = requests.get('https://www.druidai.com/careers',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', class_='job')

    lst_with_data = []

    for dt in soup_data:
        location = dt.get('data-location', '')
        if 'Romania' not in location:
            continue

        position = dt.get('data-position') or dt.find('p', class_='job-position').text
        link = dt.get('href')
        city = translate_city(location.split(',')[0].strip())

        lst_with_data.append({
            "job_title": position,
            "job_link": link,
            "company": "Druid",
            "country": "Romania",
            "city": city,
            "county": get_county(city)
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Druid'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Druid',
                  'https://www.druidai.com/hubfs/druid-logo-dark.svg'
                  ))