#
#
#
# New scraper for -> Ciklum
# Ciklum page -> https://explore-jobs.ciklum.com/en/sites/ciklum-career/jobs
#

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#


API_URL = 'https://ialmme.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions'
SITE_NUMBER = 'CX_1001'
LOCATION_ID = '300000000468495'
PAGE_SIZE = 24
FACETS = 'TITLES;LOCATIONS;LOCATION_LEVEL1;LOCATION_LEVEL2;LOCATION_LEVEL3;CATEGORIES;POSTING_DATES;WORK_LOCATIONS;FLEX_FIELDS;ORGANIZATIONS;WORKPLACE_TYPES'


def normalize_remote(workplace_type: str) -> list[str]:
    normalized = (workplace_type or '').strip().lower()

    if normalized == 'remote':
        return ['Remote']

    if normalized == 'hybrid':
        return ['Hybrid']

    return ['on-site']


def collect_data_from_site(offset: int) -> tuple[list, int]:
    response = requests.get(
        API_URL,
        params={
            'onlyData': 'true',
            'expand': 'requisitionList.secondaryLocations',
            'finder': f'findReqs;siteNumber={SITE_NUMBER},facetsList={FACETS},limit={PAGE_SIZE},locationId={LOCATION_ID},offset={offset}'
        },
        headers=DEFAULT_HEADERS,
        timeout=30)
    response.raise_for_status()

    requisitions = response.json()['items'][0]['requisitionList']
    lst_with_data = []

    for job in requisitions:
        lst_with_data.append({
            "job_title": job['Title'].strip(),
            "job_link": f'https://explore-jobs.ciklum.com/en/sites/ciklum-career/job/{job["Id"]}',
            "company": "Ciklum",
            "country": "Romania",
            "remote": normalize_remote(job.get('WorkplaceType', ''))
        })

    return lst_with_data, len(requisitions)


def req_and_collect_data_ciklum():
    """
    Collect Romania jobs from the new Oracle Ciklum careers API.
    """

    offset = 0
    big_list_jobs = []

    while True:
        data_site, page_count = collect_data_from_site(offset)
        big_list_jobs.extend(data_site)

        if page_count < PAGE_SIZE:
            break

        offset += PAGE_SIZE

    return big_list_jobs


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


if __name__ == '__main__':
    company_name = 'Ciklum'  # add test comment
    data_list = req_and_collect_data_ciklum()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Ciklum',
                      'https://jobs.ciklum.com/wp-content/webpc-passthru.php?src=https://jobs.ciklum.com/wp-content/uploads/2017/11/Ciklum_Horizontal_Logo_RGB.png&nocache=1'
                      ))
