import requests
from bs4 import BeautifulSoup
from Crawling.mk_data import mk_data
from Crawling.mk_meta import mk_meta
import time
from multiprocessing import Pool

URL_F = 'http://shopping.naver.com/detail/detail.nhn?nv_mid='
URL_M = '&pkey='
URL_T = '&withFee='


def get_pkey(mid):
    work_list = []
    req = requests.get(URL_F + mid)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        valid_txt = str(soup.find('h3').find(text=True))
        if '판매중단' in valid_txt:
            tmp_list = []
            tmp_list.append(mid)
            tmp_list.append(True)
            work_list.append(tmp_list)
            return work_list
    except:
        try:
            valid_txt = soup.find_all('h2')[3].find(text=True)
            if '상품이' in valid_txt:
                tmp_list = []
                tmp_list.append(mid)
                tmp_list.append(True)
                work_list.append(tmp_list)
                return work_list
        except:
            tmp_list = []
            tmp_list.append(mid)
            tmp_list.append(True)
            work_list.append(tmp_list)
            return work_list


    try:
        option_list = soup.find_all('div', class_='condition_group')[1].findChildren(recursive=False)[
            1].findChildren(recursive=False)
        for item in option_list:
            tmp = str(item.get('data-filter-value'))
            if tmp != '':
                tmp_list = []
                tmp_list.append(mid)
                tmp_list.append(tmp)
                tmp_list.append(str(item.findChildren(recursive=False)[2].findChildren(recursive=False)[1].find(text=True)))
                work_list.append(tmp_list)
    except:
        tmp_list = []
        tmp_list.append(mid)
        tmp_list.append('')
        work_list.append(tmp_list)
    return work_list

def Crawl(work_list):
    if work_list[1] == True:
        data = mk_data('', '', work_list[0], '', work_list[1])
        data.make()
        print(data.data.option_name + ' Finish!')
        return data.data.__dict__
    else:
        if work_list[1] != '':
            req_1 = requests.post(URL_F + work_list[0] + URL_M + work_list[1] + URL_T + 'False')
            req_2 = requests.post(URL_F + work_list[0] + URL_M + work_list[1] + URL_T + 'True')
            html_1 = req_1.text
            soup_1 = BeautifulSoup(html_1, 'html.parser')
            html_2 = req_2.text
            soup_2 = BeautifulSoup(html_2, 'html.parser')
            meta = mk_meta(soup_1)
            meta.make()
            data = mk_data(soup_1, soup_2, work_list[0], work_list[2], False)
        else:
            req_1 = requests.post(URL_F + work_list[0] + URL_T + 'False')
            req_2 = requests.post(URL_F + work_list[0] + URL_T + 'True')
            html_1 = req_1.text
            soup_1 = BeautifulSoup(html_1, 'html.parser')
            html_2 = req_2.text
            soup_2 = BeautifulSoup(html_2, 'html.parser')
            meta = mk_meta(soup_1)
            meta.make()
            data = mk_data(soup_1, soup_2, work_list[0], '', False)

        data.data.meta = meta.meta
        data.make()
        print(data.data.option_name + ' Finish!')
        return data.data.__dict__


if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(processes=4)
    data_list = pool.map(Crawl, get_pkey('5639964597'))
    print("--- %s seconds ---" % (time.time() - start_time))