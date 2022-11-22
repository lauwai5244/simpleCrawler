from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pprint
import time
import pandas as pd
import re
from selenium.webdriver.common.by import By
import requests

pp = pprint.PrettyPrinter(indent=4)
options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {
                                "profile.password_manager_enabled": False, "credentials_enable_service": False})


regex = re.compile('>(.*?)<')
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
data = []
data_chil = []


def clear(str):
    str = str.replace("['", "")
    str = str.replace("']", "")
    str = str.replace('["', "")
    str = str.replace('"]', "")
    str = str.replace(',', "")
    str = str.replace('~', "")
    str = str.replace("'", "")
    str = str.replace("\u3000", "\n")

    return str


driver.get("https://itouch.cycu.edu.tw/home/#/ann")  # 更改網址以前往不同網頁
time.sleep(3)

'''
# 模擬點擊
# first_buttons = driver.find_element(
#     By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[1]/div/div/div[1]/div/div[1]/a[2]')  # 徵才公告
# first_buttons.click()
# time.sleep(1)
'''
try:  # 少於50的就沒有這個按鈕
    first_buttons = driver.find_element(
        By.CLASS_NAME, "btn-info")

    first_buttons.click()  # 點解查看全部  over50
except:
    pp.pprint("have not this path")

time.sleep(1)

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}

soup = BeautifulSoup(driver.page_source, 'html.parser')
titles = soup.find_all('span', {'class': 'col01'})
nu = 0
for i in titles:
    if nu == 5:
        break
    if i.find(name="a") != None:

        text = clear(str(re.findall(regex, str(i))))
        if len(data) > 0:
            if data[0][1] == text:
                break
        data_chil.append(i.find(name="a").get('href'))

        response = requests.get(url=i.find(
            name="a").get('href'), headers=header)
        soup2 = BeautifulSoup(response.text, "html.parser")
        text2 = clear(str(re.findall(regex, str(soup2))))
        pp.pprint(text2)
        time.sleep(10)
        data_chil.append(text)
        data_chil.append(text2)
        data.append(data_chil)

        data_chil = []
    nu = nu + 1


data2 = pd.DataFrame(data)
data2.to_excel('notice.xlsx', sheet_name='sheet1',
               index=False, header=None)
driver.close()  # 關閉瀏覽器視窗
