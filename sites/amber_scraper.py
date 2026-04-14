#
#
#
# New scraper for -> Amber
# Amber page -> https://jobs.jobvite.com/amberstudiocareers/jobs/positions

#

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
    and collect data from Amber API.
    """

    response = requests.get('https://jobs.jobvite.com/amberstudiocareers/search?q=romania',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', class_='job-item')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('div', class_='jv-job-list-location').text.strip()
        title = dt.find('div', class_='jv-job-list-name').text.strip()
        link = dt.find('a', class_='jv-button jv-button--hollow flex-row flex-m-space-between flex-c-center')[
            'href']
        if 'romania' in location.lower():
            location = location.split(',\n')

            city = translate_city(location[1].strip())
            county = get_county(city)
            lst_with_data.append({
                "job_title": title,
                "job_link": 'https://jobs.jobvite.com/' + link,
                "company": "Amber",
                "country": "Romania",
                "city": city,
                "county": county,
                "remote": ['']
            })
            for item in lst_with_data:

                if item['city'][0].strip() == 'Hybrid Remote':
                    item['remote'] = ['Hybrid', 'Remote']
                elif item['city'][0].strip() == 'Remote':
                    item['remote'] = ['Remote']
                else:
                    item['remote'] = ['on-site']

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Amber'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Amber',
                  'https://mma.prnewswire.com/media/1633540/Amber_Logo.jpg?w=200'
                  ))
