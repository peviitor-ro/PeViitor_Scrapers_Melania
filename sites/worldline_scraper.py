#
#
#
# New scraper for -> Worldline
# Worldline page -> https://careers.worldline.com/en

#
import re

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def req_and_collect_data_():
    """
    ... this func() make a simple requests
    and collect data from Worldline API.
    """

    response = requests.get(
        'https://careers.worldline.com/en/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Keywords=Romania=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=1&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=',
        headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('a', href=True)

    lst_with_data = []

    for dt in soup_data:
        title = dt.find('h3')
        link = dt['href']
        location = dt.find('span')
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title.text,
            "job_link": 'https://careers.worldline.com/' + link.split('"')[1],
            "company": "Worldline",
            "country": "Romania",
            "city": location.text.split(',')[0]
        })

        for job in lst_with_data:
            if job['city'] == 'Multiple locations':
                job['city'] = 'Bucuresti'

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Worldline'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Worldline',
                  'https://www.parking.net/upload/banners/Links/worldline/logoworldline1.png'
                  ))
