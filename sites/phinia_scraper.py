#
#
#
#
# Company -> Phinia
# Link ----> https://phinia.wd5.myworkdayjobs.com/PHINIA_Careers?locations=f6fd9224b4eb10020afd8f5ea4390000&locations=f6fd9224b4eb10020afe120ebc820000
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
#
import uuid
#
import re

# -------> !
session = requests.Session()


def get_ids() -> tuple:
    '''
    Get all needed ids for this site.
    '''

    response = session.head(
        url='https://phinia.wd5.myworkdayjobs.com/PHINIA_Careers?locations=f6fd9224b4eb10020afd8f5ea4390000&locations=f6fd9224b4eb10020afe120ebc820000',
        headers=DEFAULT_HEADERS).headers

    play_session = re.search(r"PLAY_SESSION=([^;]+);", str(response)).group(0)
    csrf_token = re.search(r"CALYPSO_CSRF_TOKEN=([^;]+);", str(response)).group(0)
    ts_id = re.search(r"TS014c1515=([^;]+);", str(response)).group(0)
    wday_vps = re.search(r"wday_vps_cookie=([^;]+);", str(response)).group(0)
    wd_browser_id = re.search(r"wd-browser-id=([^;]+);", str(response)).group(0)

    return play_session, csrf_token, ts_id, wday_vps, wd_browser_id


def prepare_post() -> tuple:
    '''
    Here prepare post request headers.
    '''

    play_session, csrf_token, ts_id, wday_vps, wd_browser_id = get_ids()

    url = 'https://phinia.wd5.myworkdayjobs.com/wday/cxs/phinia/PHINIA_Careers/jobs'

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': f'{wday_vps} timezoneOffset=-180; {play_session} {ts_id} {wd_browser_id} {csrf_token[:-1]}',
        'Origin': 'https://phinia.wd5.myworkdayjobs.com',
        'Referer': 'https://phinia.wd5.myworkdayjobs.com/PHINIA_Careers?locations=f6fd9224b4eb10020afd8f5ea4390000&locations=f6fd9224b4eb10020afe120ebc820000',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-CALYPSO-CSRF-TOKEN': f'{csrf_token.split("=")[1]}'
    }

    data = {
        "appliedFacets": {
            "locations": ["f6fd9224b4eb10020afd8f5ea4390000", "f6fd9224b4eb10020afe120ebc820000"]
        },
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    return url, headers, data


def get_data_from_phinia():
    '''
    ... get all data from site, after post requests with fresh cookie data.
    '''
    url, headers, data = prepare_post()

    response = session.post(url=url, headers=headers, json=data).json()

    lst_with_data = []
    for job in response['jobPostings']:
        city = job['locationsText'].split('-')[0].strip()
        lst_with_data.append({
            "id": str(uuid.uuid4()),
            "job_title": job['title'],
            "job_link": 'https://phinia.wd5.myworkdayjobs.com/en-US/PHINIA_Careers' + job['externalPath'],
            "company": "Phinia",
            "country": "Romania",
            "city": city
        })

    return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Phinia'
data_list = get_data_from_phinia()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Phinia',
                  'https://www.phinia.com/ResourcePackages/Phinia/dist/708ef1de64cb6bde2362.png'
                  ))
