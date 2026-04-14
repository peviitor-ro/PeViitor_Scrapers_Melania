#
#
#
# New scraper for -> Acrelec
# Acronis job page -> https://acrelec.com/jobboard/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from _county import get_county, translate_city
#
import requests
from bs4 import BeautifulSoup


def request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from Acronis API.
    """

    response = requests.get('https://acrelec.com/jobboard/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('li', class_='jobSingle')

    lst_with_data = []

    for dt in soup_data:

        # check if Romania in location
        location = dt.find('span', class_='jobSingle-metaSingle jobSingle-location').text

        if 'Romania' in location or 'România' in location:
            link = dt.find('a')['href']
            title = dt.find('h3').text
            city = translate_city(location.split('-')[0].strip())
            county = get_county(city)

            lst_with_data.append({
                "job_title": title,
                "job_link": link,
                "company": "Acrelec",
                "country": "Romania",
                "city": city,
                "county": county,
            })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Acrelec'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Acrelec',
                  'https://acrelec.com/wp-content/uploads/2020/09/LOGO_ACRELEC_BOLD_NOIR_HD.png'
                  ))




