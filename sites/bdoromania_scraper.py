#
#
#
# New scraper for -> BDORomania
# BDORomania page -> https://www.bdo.ro/ro-ro/cariere/jobs
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
#
import requests
#


API_URL = 'https://www.bdo.ro/api/ro-ro/Careers/c5854e66-3d76-4bf4-ad2b-5cd408e9709f/Get'
CITY = 'Bucuresti'
COUNTY = 'Bucuresti'


def req_and_collect_data_():
    """
    Collect all job data from the new BDO careers API.
    """

    response = requests.get(
        API_URL,
        params={
            'currentPage': 1,
            'pageSize': 20
        },
        timeout=30)
    response.raise_for_status()

    jobs = response.json()['data']
    lst_with_data = []

    for job in jobs:
        lst_with_data.append({
            "job_title": job['title'].strip(),
            "job_link": 'https://www.bdo.ro' + job['applyURL'],
            "company": "BDORomania",
            "country": "Romania",
            "city": CITY,
            "county": COUNTY
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
    company_name = 'BDORomania'  # add test comment
    data_list = req_and_collect_data_()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('BDORomania',
                      'https://www.bdo.ro/bdokit/assets/img/BDO_logo_150dpi_RGB_290709.jpg'
                      ))
