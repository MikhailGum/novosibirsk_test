import requests, re, time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def get_data(url):
    id_kvartiri = int(re.search(r'/view/\d+', url)[0].lstrip('/view/'))
    r = requests.get(url, headers={'User-Agent': UserAgent().ie})
    respouns = r.text
    soup = BeautifulSoup(respouns, 'html.parser')
    # адрес - <span class="ui-kit-link__inner" _v-689e5c11="">Адриена Лежена, 33</span>
    adress_tag = soup.find('a', attrs={'class':'ui-kit-link slider-section-header__link _type-common _color-black'})
    adress = adress_tag.string
    # общая площадь квартиры - <span class="card-living-content-params-list__value" data-test="offer-card-param-total-area">36,5&nbsp;м<sup>2</sup></span>
    square_tag = soup.find('span', attrs={'data-test':'offer-card-param-total-area'})
    square = float(square_tag.text.rstrip('м2').replace(' ','').replace(',', '.'))
    # этаж - <span class="card-living-content-params-list__value" data-test="offer-card-param-floor">9 из 17</span>
    floor_tag = soup.find('span', attrs={'data-test':'offer-card-param-floor'})
    floor = int(re.search(r'\d+ из ', floor_tag.text)[0].replace(' из ', ''))
    # год сдачи - <span class="card-living-content-params-list__value">2021 г.</span>
    try:
        # year_tag = soup.find_all('span', attrs={'class':'card-living-content-params-list__value'})
        # year = int(year_tag[6].text.rstrip(' г.'))
        div_tag = soup.find('div', attrs={'class': 'card-living-content-params__col _last'})
        span_tag = div_tag.find('span', attrs={'class': 'card-living-content-params-list__value'})
        year = int(span_tag.text.rstrip(' г.'))
    except:
        year = 0
    # цена - <span data-v-6c899776="" class="price">3 480 000 ₽</span> float(kvartiri_link.rstrip('₽').replace(' ', ''))
    price_tag = soup.find('span', attrs={'class':'price'})
    price = float(price_tag.text.rstrip('₽').replace(' ', ''))
    # материал дома - <span class="card-living-content-params-list__value" data-test="offer-card-param-house-material-type">панель</span>
    material_tag = soup.find('span', attrs={'data-test':'offer-card-param-house-material-type'})
    material = material_tag.text
    # локация объекта
    pattern = re.compile('\"latitude\":\d{2}.\d+,\"longtitude\":\d{2}.\d+')
    location_re = re.search(pattern, respouns)
    # print(location_re)
    location = location_re[0] # "latitude":55.03660423746987,"longtitude":82.98967792065328
    # дата текущая 
    date = time.strftime('%Y-%m-%d', time.gmtime())
    #Формирование кортежа с данными о квартире в формате ()
    data_kvartira = (id_kvartiri, adress, square, floor, year, price, material, location, date)
    return data_kvartira

# url = 'https://novosibirsk.n1.ru/view/72862864/'
# print(get_data(url))

# with open('kvartiri_link.txt', 'r') as f:
#     kvartiri_links = f.read().split('\n')
# # url = 'https://novosibirsk.n1.ru/view/73696905/'
# kvartira_data = []
# for link in kvartiri_links:
#     try:
#         kvartira_data.append(get_data(link))
#     except:
#         kvartira_data.append(link)
#     time.sleep(1)
#     print(link)
    
# print(kvartira_data)
