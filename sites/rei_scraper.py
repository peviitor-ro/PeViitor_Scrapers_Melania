#
#
#
# New scraper for -> REI
# REI job page -> https://rei-d-services.com/en/careers

#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid


def request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get('https://rei-d-services.com/en/careers',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', class_='post-entry-content')

    lst_with_data = []

    for dt in soup_data:
        link = dt.find('a')['href']
        title = dt.find('a').text

        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "REI",
            "country": "Romania",
            "city": "Romania"
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'REI'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('REI',
                  'https://rei-d-services.com/wp-content/uploads/2020/01/logo-300x184.png'
                  ))

