from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def amazon(driver, wait, category):
    driver.get('https://amazon.co.jp/')

    try:
        element = driver.find_element(By.XPATH, '//*[@id="navbar-backup-backup"]/div/div[1]/a[2]')
        element.click()
    except:
        pass
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "ランキング")))
    element.click()
    time.sleep(3)
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, category)))
    element.click()

    amazon_data = []
    seller_names = []

    for x in range(0,2):
        trial_times = 1
        for i in range(0, 50):
            asin_index = f"p13n-asin-index-{i}"
            not_found = True
            seller_name = ''

            while not_found:
                try:
                    element = driver.find_element(By.ID, asin_index)
                    text = element.text
                    if 'Amazon' in text or '取り扱っていません' in text:
                        break
                    element.click()
                    wait.until(EC.element_to_be_clickable((By.ID, 'acrCustomerReviewLink')))
                    product_title = driver.find_element(By.ID, 'productTitle').text
                    url = driver.current_url
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="newAccordionRow"]/div/div[1]/i')
                        element.click()
                        time.sleep(1)
                    except:
                        pass
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="sellerProfileTriggerId"]')
                        seller_name = element.text
                        if seller_name in seller_names:
                            driver.back()
                            break
                    except:
                        driver.back()
                        break
                    seller_names.append(seller_name)
                    element.click()
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[2]/span[2]')
                        name = element.text
                    except:
                        name = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[3]/span[2]')
                        phone = element.text
                    except:
                        phone = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[5]/span')
                        address_1 = element.text
                    except:
                        address_1 = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[6]/span')
                        address_2 = element.text
                    except:
                        address_2 = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[7]/span')
                        address_3 = element.text
                    except:
                        address_3 = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[8]/span')
                        address_4 = element.text
                    except:
                        address_4 = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[9]/span')
                        address_5 = element.text
                    except:
                        address_5 = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[10]/span')
                        address_6 = element.text
                    except:
                        address_6 = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[11]/span[2]')
                        person_in_charge = element.text
                    except:
                        person_in_charge = ''
                    try:
                        element = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[12]/span[2]')
                        store_name = element.text
                    except:
                        store_name = ''

                    whole_address = address_1 + ' ' +  address_2 + ' ' + address_3 + ' ' + address_4 + ' ' + address_5 + ' ' + address_6
                    seller_info = [product_title, store_name, name, '', '', whole_address, '', '', phone, '', url, '', '', person_in_charge,'','','']
                    amazon_data.append(seller_info)
                    seller_names.append(name)
                    driver.back()
                    driver.back()
                    not_found = False
                except:
                    driver.execute_script(f"window.scrollTo(0, { 150 * trial_times});")
                    trial_times += 1
                    time.sleep(2)
                    pass
                if trial_times > 15:
                  break
            print(i)
        try:
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "2")))
            element.click()
        except:
          pass
    return amazon_data