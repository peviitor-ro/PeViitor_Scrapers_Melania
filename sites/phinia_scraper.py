#
#
#
#
# Company -> Phinia
# Link ----> https://phinia.wd5.myworkdayjobs.com/PHINIA_Careers?locations=f6fd9224b4eb10020afd8f5ea4390000&locations=f6fd9224b4eb10020afe120ebc820000
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests


API_URL = 'https://phinia.wd5.myworkdayjobs.com/wday/cxs/phinia/PHINIA_Careers/jobs'
CAREERS_URL = 'https://phinia.wd5.myworkdayjobs.com/en-US/PHINIA_Careers'
ROMANIA_LOCATIONS = [
    'f6fd9224b4eb10020afd8f5ea4390000',
    'f6fd9224b4eb10020afe120ebc820000'
]


def get_data_from_phinia():
    """
    Collect Romania jobs from the public Phinia Workday API.
    """

    response = requests.post(
        url=API_URL,
        headers=DEFAULT_HEADERS,
        json={
            'appliedFacets': {'locations': ROMANIA_LOCATIONS},
            'limit': 20,
            'offset': 0,
            'searchText': ''
        },
        timeout=30)
    response.raise_for_status()

    lst_with_data = []
    for job in response.json()['jobPostings']:
        if 'Romania' not in job.get('locationsText', ''):
            continue

        city = job['locationsText'].split('-')[0].strip()
        lst_with_data.append({
            'job_title': job['title'],
            'job_link': CAREERS_URL + job['externalPath'],
            'company': 'Phinia',
            'country': 'Romania',
            'city': city,
            'county': 'Iasi',
            'remote': ['on-site']
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
    company_name = 'Phinia'
    data_list = get_data_from_phinia()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Phinia',
                      'https://www.phinia.com/ResourcePackages/Phinia/dist/708ef1de64cb6bde2362.png'
                      ))
