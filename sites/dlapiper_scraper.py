#
#
#
# New scraper for -> DLAPiper
# DLAPiper page -> https://careers.dlapiper.com/job-search/
#

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
from _county import get_county, translate_city


API_URL = 'https://careers.dlapiper.com/system/modules/com.dlapiper.careers/functions/get-jobs.json'


def req_and_collect_data_():
    """
    Collect Romania jobs from the DLA Piper jobs API.
    """

    response = requests.post(
        API_URL,
        json={
            'country': 'Romania',
            'page': '1',
            'sort': 'by-default'
        },
        headers=DEFAULT_HEADERS,
        timeout=30)
    response.raise_for_status()

    jobs = response.json()['items']
    lst_with_data = []

    for job in jobs:
        location = job['location'].split(',')[0].strip()
        city = translate_city(location)
        county = get_county(city)

        lst_with_data.append({
            "job_title": job['title'],
            "job_link": 'https://careers.dlapiper.com' + job['url'],
            "company": "DLAPiper",
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


if __name__ == '__main__':
    company_name = 'DLAPiper'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('DLAPiper',
                      'https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/DLA_Piper_logo.svg/300px-DLA_Piper_logo.svg.png'
                      ))
