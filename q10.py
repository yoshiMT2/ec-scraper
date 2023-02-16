from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs


def get_properties(soup, url):
    try:
        product_name = soup.find('div', {'class': 'text_title'}).text.strip()
    except:
        product_name = ''
    try:
        country = soup.find('dl', {'name': 'shipping_panel_area'}).dd.text
    except:
        country = ''
    try:
        shipping_mthd = soup.find('p', {'class': 'sh_option2'}).text.split(' ')[0].strip()
    except:
        shipping_mthd = ''
    try:
        company = soup.find('div', {'id': 'ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_ctrGoodsQAInfo_SellerNmExpose'}).dd.text
    except:
        company = ''
    try:
        tel = soup.find('div', {'id': 'ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_ctrGoodsQAInfo_panSellerinfoTelno'}).dd.text
    except:
        tel = ''
    try:
        email = soup.find('div', {'id': 'ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_ctrGoodsQAInfo_PanSellerinfoEmail'}).dd.text
    except:
        email = ''
    try:
        address = soup.find('div', {'id': 'ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_ctrGoodsQAInfo_PanSellerinfoAddress'}).dd.text.replace('\n', ' ')
    except:
        address = ''
    try:
        contact_hour = soup.find('div', {'id': 'ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_ctrGoodsQAInfo_panAvailableDuring'}).dd.text.replace('\n', ' ')
    except:
        contact_hour = ''

    data_arr = [product_name, company, company, country, shipping_mthd, address, email, contact_hour, tel, '', url]

    return data_arr

def q10(driver):

    driver.get('https://www.qoo10.jp/')

    element = driver.find_element(By.LINK_TEXT, 'ランキング')
    element.click()
    time.sleep(5)

    soup = bs(driver.page_source, 'html.parser')
    item_list = soup.find("div", {"class":"bd_glr_best"})
    items = item_list.find_all("a", {"class": "thmb"})

    companies = []
    whole_data = []

    for item in items:
        url = item['href']
        driver.get(url)
        soup = bs(driver.page_source, 'html.parser')
        try:
            company = soup.find('div', {'id': 'ctl00_ctl00_MainContentHolder_MainContentHolderNoForm_ctrGoodsQAInfo_SellerNmExpose'}).dd.text
        except:
            continue
        if company in companies:
            continue
        companies.append(company)
        soup_data = get_properties(soup, url)
        whole_data.append(soup_data)

        print(len(companies))

    return whole_data