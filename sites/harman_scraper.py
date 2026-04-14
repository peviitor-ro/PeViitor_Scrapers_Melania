#
#
#
# New scraper for -> Harman
# Harman page -> https://harmanglobal.avature.net/careers
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
from _county import get_county, translate_city


def req_and_collect_data_harman():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get(
        'https://jobsearch.harman.com/en_US/careers/SearchJobs/?2039=%5B59997%5D&2039_format=2669&listFilterMode=1&jobRecordsPerPage=20&',
        headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='article__header__text')

    lst_with_data = []

    for dt in soup_data:
        location = dt.find('span', class_='list-item-location').text.split(',')
        city = translate_city(location[0].split(':')[-1].split('-')[-1].strip())
        county = get_county(city)
        title = dt.find('a').text
        link = dt.find('a')['href']

        lst_with_data.append({
            "job_title": title.strip(),
            "job_link": link,
            "company": "Harman",
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


company_name = 'Harman'  # add test comment
data_list = req_and_collect_data_harman()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Harman',
                  'https://news.harman.com/media/themes/5e30ae5f2cfac23c3e118f1b/images/HARMAN-logo.png'
                  ))
