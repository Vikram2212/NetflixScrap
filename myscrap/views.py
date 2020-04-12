from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models
BASE_URL = 'https://www.netflix.com/search?q={}'

def home(request):
    return render(request,'home.html')

def searching(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    finalurl = BASE_URL.format(quote_plus(search))

    cookies = {
        'clSharedContext': '80f663eb-2f8f-4611-9ab8-2e9252cca7c3',
        'memclid': '03dcc131-e481-4432-8695-b43b6e9babe9',
        'flwssn': '0039b623-187c-4918-ab7a-856eb255e163',
        'lhpuuidh-browse-MOUGNNBEJZBSZEONYJJTVJZPSI': 'IN%3AEN-IN%3A8b8d9681-2c61-4ae3-918f-302fbe8988f0_ROOT',
        'lhpuuidh-browse-MOUGNNBEJZBSZEONYJJTVJZPSI-T': '1586677001779',
        'lhpuuidh-browse-Q5YWT7OKZFHB3KEHDYJVP62PTA': 'IN%3AEN-IN%3A876d7e3a-35c8-419a-a7d0-cfa1889e4b57_ROOT',
        'lhpuuidh-browse-Q5YWT7OKZFHB3KEHDYJVP62PTA-T': '1586677939773',
        'nfvdid': 'BQFmAAEBEPUnbYHnFHy1Nc2XNsTtGg1gM77krcBwpVHZHJY3egv%2B2r2cCTUEk0onl986FuEPObBjook3fvuGur6aAvEqj7k4NSY0KXeyvAkWnM3DyRdXWszEVX16u2RrL08w9e%2B%2FiyzywLgpQERLL3J1DmL%2Bs9AE',
        'profilesNewSession': '0',
        'cL': '1586686636895%7C158668663696636368%7C15866866364755302%7C%7C4%7Cundefined',
        'SecureNetflixId': 'v%3D2%26mac%3DAQEAEQABABS2e_0NGy5zvlnwBMEBK06gS5W8Ea3PSM8.%26dt%3D1586687343217',
        'NetflixId': 'v%3D2%26ct%3DBQAOAAEBEFkr_WnfcyCP9gerWlPPbo2BwDkWRnfFmg97hQhMO3U7beSCWD1MPR2MQCEcoBTQvkqcKKbRvnlej5_WwQlewl3_S_0dAHZbGlott2109C9gW9GcWIqcY6HYjXvjtwywMbybeEfM3utYAeyMIcS9UHhghnu9TSmUspWLU_FzOboJxZ8XURZkqOwcKdeqR6vTqrL3MZKlbChpxfJ8fDurq5Zh1nzzBZfIPnayP_ERatm7JNW6SDm-KYEqtF2ZcSmx4x-PMYa6NtYDpdQx4Xd5RrUPWPSiL2RQIso2kx8MnGJ7QO0K8dGEZKH6XUTcQqTi0IV8vgrErXtN43UXj7Ib3I3jQvwwIwmO5Ymm7gX1syOHuZw6SILFmul3BGl4GD1bZdxdiJ8Q5UWvymrkjXPs0P4GpLss5ODMqCVnk_MoLXrKsGUS2jf6ur6eJjCDNCN2jNqV1p_JIM852jlQmKlbjjTB5CN_-tHSPC5fVvcUODvxdIMYKp_LtkdWXxCakG08tUXCUmERKYLD5OtRZEHq_GgqtuxgQqzesWArF5pADB0wV4CMwLDHEMQSc81waCP-aGL8FR6zzqVQtGdpLhmsTpm6DAOaRtOJOWLjCn7vjgUKWaE.%26bt%3Ddbl%26ch%3DAQEAEAABABT88qclwPCVWmIjm3EkXyvSal_o0QZOe4U.%26mac%3DAQEAEAABABQaeTPgrxI3Zdf2SQ4QsdQ_hf9mlfFokrs.',
        'playerPerfMetrics': '%7B%22uiValue%22%3A%7B%22throughput%22%3A4022%2C%22throughputNiqr%22%3A0.7659016310193755%7D%2C%22mostRecentValue%22%3A%7B%22throughput%22%3A4022%2C%22throughputNiqr%22%3A0.7659016310193755%7D%7D',
    }

    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    response = requests.get(finalurl , headers=headers, cookies=cookies)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    finding = soup.find_all('div',{'class':'slider-item'})

    final_listings = []
    for post in finding:
        post_title = post.find(class_='fallback-text').text
        post_url = post.find('a').get('href')
        post_img = post.find('img').get('src')

        final_listings.append((post_title,post_url,post_img))

    frontend = {
        'search': search,
        'final_listings': final_listings
    }


    return render(request, 'myscrap/search.html', frontend)