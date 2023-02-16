from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup as bs

COLUMN_NAMES = ['category', 'store_name', 'company_name', 'shipped_from',
                    'transporter', 'address', 'email', 'service_hour', 'tel',
                    'fax', 'product_url', 'open_date', 'office_hour', 'staff',
                    'staff_email', 'staff_tell', 'response']

def suning(driver, wait):

    driver.get('https://www.suning.com/')
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div[2]/div/div[1]/a[1]')))
    element.click()
    driver.switch_to.window(driver.window_handles[1])

    i = 1
    j = 1
    sung_data = []
    has_items = True

    while has_items:

        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[4]/div[2]/div/div/div[{i}]/div/div[2]/div/ul/li[{j}]/a')))
            element.click()
            driver.switch_to.window(driver.window_handles[2])

        except:
            i += 1
            j = 1
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[4]/div[2]/div/div/div[{i}]/div/div[2]/div/ul/li[{j}]/a')))
                continue
            except:
                has_items = False

        has_next = True
        iteration = 1

        while has_next:
            company = ""
            phone = ""
            try:
                driver.switch_to.window(driver.window_handles[2])
                element = wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[4]/div/div/div/div[1]/div/div[2]/div/ul/li[{iteration}]/a')))
                element.click()
                time.sleep(1)
                driver.execute_script(f"window.scrollTo(0, 600);")
                driver.switch_to.window(driver.window_handles[3])
                soup = bs(driver.page_source, 'html.parser')

            except:
                has_next = False
            try:
                product = soup.find('div', {'class':'proinfo-title'}).find_all('li')[1].text
            except:
                product = ''
            try:
                company = soup.find('div',{'JS_storename'}).text.strip()
            except:
                pass
            try:
                el = soup.find('div', {'class': 'si-intro' }).find_all('p')[0].text
                if int(el)>0:
                    phone = el

            except:
                pass
            if company or phone:
                url = driver.current_url

                data = [product, company, company, '', '', '', '', '', phone, '', url,'','','','','','']
                sung_data.append(data)
            iteration += 1
            driver.close()
            print(i, j)
        driver.switch_to.window(driver.window_handles[1])
        j += 1


    df = pd.DataFrame(sung_data)
    df.columns = COLUMN_NAMES
    new_df = df.drop_duplicates(subset=['company_name'])
    data_suning = new_df.to_numpy().tolist()

    return data_suning
