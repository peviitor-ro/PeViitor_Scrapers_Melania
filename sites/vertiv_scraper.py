#
#
#
#
# New scraper for -> Vertiv
# Vertiv job page -> https://egup.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/requisitions?location=Romania&locationId=300000000271023&locationLevel=country&mode=location
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
#
import requests


API_URL = 'https://egup.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=100,locationId=300000000271023,sortBy=POSTING_DATES_DESC'
JOB_URL = 'https://egup.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/requisitions/preview/'


def has_romania_location(job):
    primary_location = job.get('PrimaryLocation', '')
    if 'Romania' in primary_location:
        return True

    for location in job.get('secondaryLocations', []):
        if location.get('CountryCode') == 'RO':
            return True

    return False


def get_city(job):
    primary_location = job.get('PrimaryLocation', '')
    if 'Romania' in primary_location:
        city = primary_location.split(',')[0].strip()
        if city == 'Romania':
            return 'Cluj Napoca'
        return city

    for location in job.get('secondaryLocations', []):
        if location.get('CountryCode') == 'RO':
            city = location.get('Name', 'Cluj Napoca').split(',')[0].strip()
            if city == 'Romania':
                return 'Cluj Napoca'
            return city

    return 'Cluj Napoca'


def request_and_collect_data():
    """
    Collect all Vertiv jobs that are available in Romania.
    """

    response = requests.get(url=API_URL,
                            headers=DEFAULT_HEADERS,
                            timeout=30)
    response.raise_for_status()
    requisitions = response.json()['items'][0]['requisitionList']

    lst_with_data = []

    for job in requisitions:
        if not has_romania_location(job):
            continue

        job_id = job['Id']
        city = get_city(job)
        lst_with_data.append({
            'job_title': job['Title'],
            'job_link': f'{JOB_URL}{job_id}',
            'company': 'Vertiv',
            'country': 'Romania',
            'city': city,
            'county': 'Cluj',
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
    company_name = 'Vertiv'  # add test comment
    data_list = request_and_collect_data()
    scrape_and_update_peviitor(company_name, data_list)

    print(update_logo('Vertiv',
                      'https://www.vertiv.com/Content/images/logo_AoC_gray.svg'
                      ))
