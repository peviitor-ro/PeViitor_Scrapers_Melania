#
#
#
#
#
# New scraper for -> HRSRomania
# HRSRomania page -> https://www.hrsro.com/
#
#
import requests
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from time import sleep
import uuid

session = requests.Session()


def get_php_id() -> str:
    '''
    This func return session ID.
    '''

    s_id = session.head('https://www.hrsro.com/',
                        headers=DEFAULT_HEADERS).headers['Set-Cookie'].split()[0]

    return s_id


CONST_ID = get_php_id()


def prepare_post_req(num_page: str) -> tuple:
    '''
    Post req.
    '''

    url = 'https://www.hrsro.com/ajax/filter/?l=en'

    headers = {
        'authority': 'www.hrsro.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': f'{CONST_ID[:-1]}',
        'origin': 'https://www.hrsro.com',
        'referer': f'https://www.hrsro.com/en/jobs?keyword=&show-items=10&page={num_page}',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'keyword': '',
        'show-items': '10',
        'page': f'{num_page}'
    }

    return url, headers, data


def collect_data_hrs():
    '''
    ... get data from site.
    '''
    url, headers, data = prepare_post_req('1')

    num_pages = session.post(url=url, headers=headers, data=data).json()['positions_count']
    num_for = num_pages // 10 + 1

    lst_with_data = []
    for page in range(1, num_for + 1):

        urls, headerss, datas = prepare_post_req(str(page))
        jobs_json = session.post(url=urls, headers=headerss, data=datas).json()['positions']

        for job in jobs_json:
            location = job['location']
            if location == 'Remote':
                lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": job['title'],
                    "job_link": job['item_link'],
                    "company": "HRSRomania",
                    "country": "Romania",
                    "remote": job['location']
                })
            else:
                lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": job['title'],
                    "job_link": job['item_link'],
                    "company": "HRSRomania",
                    "country": "Romania",
                    "city": job['location']
                })

            for dict in lst_with_data:
                if dict.get('city') is None:
                    dict['city'] = 'Romania'

        # sleep, Not block me!
        sleep(1)

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'HRSRomania'  # add test comment
data_list = collect_data_hrs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('HRSRomania',
                  'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiTHQGg18vALX40onszHcHnc5kjPgPxtAKtHMMbN-uXQ&s'
                  ))
