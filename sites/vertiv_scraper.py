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
import uuid


def request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from API.
    """

    response = requests.get(
        url='https://egup.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=100,locationId=300000000271023,sortBy=POSTING_DATES_DESC',
        headers=DEFAULT_HEADERS).json()['items']

    lst_with_data = []

    for item in response:
        for job in item['requisitionList']:
            job_id = job['Id']
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": job['Title'],
                "job_link": f'https://egup.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/requisitions/preview/{job_id}',
                "company": "Vertiv",
                "country": "Romania",
                "city": job['PrimaryLocation'].split(',')[0]
            })

        # because there are a lot of jobs without city, only 'Romania', and the company has the office at Cluj Napoca, and the jobs are not 'Remote'
        # for all the cities with 'Romania' are changed with 'Cluj Napoca'
        for itm in lst_with_data:

            if itm['city'] == 'Romania':
                itm['city'] = 'Cluj Napoca'

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Vertiv'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Vertiv',
                  'https://www.vertiv.com/Content/images/logo_AoC_gray.svg'
                  ))