from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import pandas as pd

COLUMN_NAMES = ['category', 'store_name', 'company_name', 'shipped_from',
                    'transporter', 'address', 'email', 'service_hour', 'tel',
                    'fax', 'product_url', 'open_date', 'office_hour', 'staff',
                    'staff_email', 'staff_tell', 'response']

def get_urls(driver):

    driver.get('https://www.gome.com.cn/')
    screen_height = 1000
    urls = []

    for i in range(0, 6):
        driver.execute_script(f"window.scrollTo(0,{ screen_height });")
        time.sleep(2)

        has_next = True
        tab_num = 2
        soup = bs(driver.page_source, 'html.parser')
        tags = soup.find('ul', {'class': 'mc_r_inner'}).find_all('a')
        for tag in tags:
            urls.append(tag['href'])
        while has_next:
            try:
                element = driver.find_element(By.XPATH, f'/html/body/div[9]/div[{i+1}]/div/div[1]/ul/li[{tab_num}]/a')
                element.click()
                time.sleep(0.5)
                tab_num += 1
                time.sleep(0.5)
            except:
                has_next = False
        screen_height += 550


    soup = bs(driver.page_source, 'html.parser')
    all_ul = soup.find_all('ul', {'class': 'main_inner'})
    for ul in all_ul:
        tags = ul.find_all('a')
        for tag in tags:
            if '国美' in tag['title']:
                continue
            url = 'https:' + tag['href']
            urls.append(url)

    product_urls = [*set(urls)]

    return product_urls

def gome(driver):
    urls = get_urls(driver)
    print(f'The number of urls is {len(urls)}.')
    list_data = []
    i = 1
    for url in urls:
        print(i)
        i += 1
        try:
          driver.get(url)
        except:
          continue
        time.sleep(1)
        try:
            element = driver.find_element(By.CLASS_NAME, 'pop-stores-others')
        except:
            continue
        page_url = driver.current_url
        soup = bs(driver.page_source, 'html.parser')
        try:
            product_name = soup.find('div', {'class':'hgroup'}).find('h1').text.strip()
        except:
            product_name = ''
        try:
            store_name = soup.find('a',{'class':'name'}).text
        except:
            store_name = ''
        try:
            phone = soup.find('span', {'class':'txt-phone'}).text
        except:
            phone = ''
        try:
            p_tags = soup.find('div', {'class':'company-wrapper'}).find_all('p')
        except:
            pass
        try:
            company_name = p_tags[0].text.split('：')[1].strip()
        except:
            company_name = ''
        try:
            place = p_tags[1].text.split('：')[1].strip()
        except:
            place = ''
        payload = [product_name, store_name, company_name, '', '', place, '', '', phone, '', page_url, '', '', '', '', '', '' ]
        list_data.append(payload)

    df = pd.DataFrame(list_data)
    df.columns = COLUMN_NAMES
    new_df = df.drop_duplicates(subset=['company_name'])
    data_gome = new_df.to_numpy().tolist()

    return data_gome