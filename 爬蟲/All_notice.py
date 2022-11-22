from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pprint
import time
import pandas as pd
import re
from selenium.webdriver.common.by import By
pp = pprint.PrettyPrinter(indent=4)
options = Options()
data = []
data_chil = []
i = 0


def clear(str):
    str = str.replace("['", "")
    str = str.replace("']", "")
    str = str.replace('["', "")
    str = str.replace('"]', "")
    return str


regex = re.compile('>(.*?)<')
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {
                                "profile.password_manager_enabled": False, "credentials_enable_service": False})


driver = webdriver.Chrome('./chromedriver', chrome_options=options)

driver.get("https://ann.cycu.edu.tw/aa/")  # 更改網址以前往不同網頁
time.sleep(2)


def Craw(data_chil, i, data, driver, regex):

    # 模擬點擊
    first_buttons = driver.find_element(
        By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[1]/div[6]/div[2]/span/select/option[18]')
    first_buttons.click()

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    titles = soup.find_all('div', {
        'class': 'tjs_cell_text_00'})
    for item in titles:
        if "text_align_left" in str(item):
            text = clear(str(re.findall(regex, str(item))))
            pp.pprint(str(i) + text)
            i = i + 1
            data_chil.append(text)

        if(i % 3 == 0):
            if len(data_chil) > 0:
                data.append(data_chil)
                data_chil = []


for x in range(0, 4):
    data_chil = []
    Craw(data_chil, i, data, driver, regex)
    next_buttons = driver.find_element(
        By.CLASS_NAME, 'tjs_cell_icon_next')
    next_buttons.click()
    time.sleep(2)


data2 = pd.DataFrame(data)
data2.to_excel('test.xlsx', sheet_name='sheet1',
               index=False, header=None)
driver.close()  # 關閉瀏覽器視窗
