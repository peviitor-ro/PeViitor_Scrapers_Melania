#
#
#
#
# New scraper for -> Bookster
# Bookster job page -> https://cariere.bookster.ro/
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

    response = requests.get(url='https://cariere.bookster.ro/api/jobs/list',
                            headers=DEFAULT_HEADERS).json()

    lst_with_data = []

    for job in response:
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": job['Title'],
            "job_link": 'https://cariere.bookster.ro/view/' + job['Slug'],
            "company": "Bookster",
            "country": "Romania",
            "city": "Bucuresti"
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Bookster'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Bookster',
                  'https://cariere.bookster.ro/Content/img/logo-text-r.svg'
                  ))
