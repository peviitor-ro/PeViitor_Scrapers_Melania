#
#
#
# New scraper for -> Webmarc
# Webmarc page -> https://webmarc.io/hiring
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
    and collect data from Webmarc API.
    """

    response = requests.get('https://webmarc.io/hiring',
                            headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div',
                              class_='jobcard_job-card-wrapper__TqKvb job-card flex-wrap-xs relative bg-background-light px-sm-20 py-xs-16 mb-30 mb-sm-35')

    lst_with_data = []

    for dt in soup_data:
        id = dt['id']
        match = re.search(r'\d+', id)

        if match:
            number = match.group()
            location = dt.find('p', class_='jobcard_job-card-subtitle__Yx_4O').text.split('-')[0].strip()
            title = dt.find('p', class_='jobcard_job-card-title__mElbr').text
            lst_with_data.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": 'https://webmarc.io/job/' + number,
                "company": "Webmarc",
                "country": "Romania",
                "city": location
            })

            for item in lst_with_data:
                if item.get('city') == 'Remote':
                    item['remote'] = item.pop('city')
                else:
                    return lst_with_data

        return lst_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Webmarc'  # add test comment
data_list = req_and_collect_data_()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Webmarc',
                  'data:image/jpeg;base64,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7GRwva+JgYLMIz2t/Ef9fIKvRHSg+wxPktm45UMw+ngZYT07zpy5R8LNMRgDzsDv5rx/UGIPkjkLog6OZszcsQFnte94P/KR5t5qqRTIp8Fxy5J82LVVRFHFUCGVkdhGHxNOQBrWWB7CzW+ovzdexYzXxTSTMmGo98by5zQ45owQ07+AJHnfe6r0VyoWtYmKXJK94TgFrS1rDTmmDA3ZsZOYgepJvzupLcermzSzDQ1JnB0rtBt3us4Enbkh7r/PxVYiOlB7oKTXcsvflcZzPmi1jLHM94haC+RhJa47bm538VphxOphpTTMczTIlG7ASBI0NeAfMAfRQ0TKhwMUuS0fj1fJNDNI6J8kJvE90LSWDwBtx3+viVGfiNS+aolc8Z6iIRSHKN2jLb5fkaoiIqUFsg5Se7Lj+0mJhz3B8QL3ukNoWj4nG5PHc7rXFjM9LTULKE6EtNG5hlABLrymS3yvb528CQqtFMmnwXHLksYMbrqeNkcD42RxlpjZpghls/APjqPvfnMpWG9VYrhcDoKB8EMLnl+RsDbAnw+ipER0act4oKclswiItpgEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREB//Z'
                  ))
