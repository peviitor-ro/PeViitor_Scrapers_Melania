#
#
# New scraper for -> Electromontaj
# Electromontaj page https://electromontaj.ro/cariere/
#
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
#
import uuid

session = requests.Session()


def request_and_collect_data():
    """
    ... this func() make a simple requests
    and collect data from Electromontaj API.
    """

    response = requests.get('https://electromontaj.ro/cariere/',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div', attrs={'class': 'elementor-cta__content'})

    lst_with_data = []

    for data in soup_data:
        title = data.find('h2', class_='elementor-cta__title elementor-cta__content-item elementor-content-item')

        if title:
            link = data.find('a', class_='elementor-cta__button elementor-button elementor-size-sm')['href']
            location = data.find('div',
                                 class_='elementor-cta__description elementor-cta__content-item elementor-content-item').text

            # Founding "Zona:"'s index
            start_index = location.find("Zona:")

            # Check if was founded "Zona:"
            if start_index != -1:

                # keep the string between "Zona:" and "Tip". There the cities are found
                end_index = location.find("Tip", start_index)
                if end_index != -1:
                    zona_text = location[start_index + len("Zona:"):end_index].strip().split()

                    lst_with_data.append({
                        "id": str(uuid.uuid4()),
                        "job_title": title.text.strip(),
                        "job_link": link,
                        "company": "Electromontaj",
                        "country": "Romania",
                        "city": zona_text
                    })

    for job in lst_with_data:
        city_list = job['city']
        if len(city_list) > 1:
            city_list[0] = city_list[0][:-1]
        if 'și' in city_list:
            index_si = city_list.index('și')
            job['city'] = city_list[:index_si]

    new_lst_with_data = [job for job in lst_with_data if 'Finlanda' not in job.get('city', [])]

    return new_lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Electromontaj'  # add test comment
data_list = request_and_collect_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Electromontaj',
                  'https://mla4lxcw4mmg.i.optimole.com/cb:7Jpy.32b98/w:391/h:184/q:mauto/ig:avif/f:best/https://electromontaj.ro/wp-content/uploads/2021/01/Logo-Electromontaj.svg'
                  ))
