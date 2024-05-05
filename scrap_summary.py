import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import time
import pandas as pd
import os

start_index = 1200
end_index = 1300
filename = "2014_2023_ForeignMovie"
data = pd.read_csv(f"{filename}.csv")
data = data[start_index:end_index]

webdriver_options = webdriver.ChromeOptions()
# webdriver_options .add_argument('headless')

driver = webdriver.Chrome(executable_path='C:/chromedriver', options = webdriver_options)
wait = WebDriverWait(driver, 5)
driver.get("https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do")

# downloading poster image
# url_list = []
# for i in range(start_index, end_index):
#     print('{}번째 영화 이미지 추출중'.format(i))
#     try:
#         driver.refresh()
#         name = wait.until(ec.visibility_of_element_located((By.XPATH, ".//div[@class='item']/div/input")))
#         name.clear()
#         name.send_keys(data['영화명'][i])
        
#         if str(data['개봉일'][i]) != 'nan':
#             start_date = wait.until(ec.visibility_of_element_located((By.ID, "cal_start")))
#             start_date.send_keys(data['개봉일'][i])
#             start_date.send_keys(Keys.ENTER)
        
#         button = wait.until(ec.visibility_of_element_located((By.XPATH, ".//button[@class='btn_blue']")))
#         ActionChains(driver).move_to_element(button)
#         button.click()
        
#         time.sleep(3)
#         info_button = wait.until(ec.visibility_of_element_located((By.XPATH, ".//span[@class='ellip']/a")))
#         info_button.click()
        
#         img_url = wait.until(ec.visibility_of_element_located((By.XPATH, ".//div[@class='item_tab basic']/div[2]/a"))).get_attribute('href')
        
#         url_list.append(img_url)
        
#     except:
#         url_list.append("None")

# data['포스터URL'] = url_list
# data.to_csv("2014_2023_ForeignMovie(2).csv", index=False, encoding='utf-8-sig')

summary_list = []
genre_list = []
for i in range(start_index, end_index):
    if i % 10 == 0:
        print(f'extract {i}-th movie summary')
    driver.refresh()
    name = wait.until(ec.visibility_of_element_located((By.XPATH, ".//div[@class='item']/div/input")))
    name.clear()
    name.send_keys(data['영화명'][i])
        
    if str(data['개봉일'][i]) != 'nan':
        start_date = wait.until(ec.visibility_of_element_located((By.ID, "cal_start")))
        start_date.send_keys(data['개봉일'][i])
        start_date.send_keys(Keys.ENTER)
    
    button = wait.until(ec.visibility_of_element_located((By.XPATH, ".//button[@class='btn_blue']")))
    ActionChains(driver).move_to_element(button)
    button.click()
        
    time.sleep(3)
    
    try:
        genre = wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[4]/table/tbody/tr[1]/td[7]/span"))).get_attribute('title')
        genre_list.append(genre)
    except:
        genre_list.append("None")
    
    try:
        info_button = wait.until(ec.visibility_of_element_located((By.XPATH, ".//span[@class='ellip']/a")))
        info_button.click()
        
        summary = wait.until(ec.visibility_of_element_located((By.XPATH, ".//p[@class='desc_info']"))).text
        summary_list.append(summary)
    except:
        summary_list.append("None")

data['줄거리'] = summary_list
data['장르'] = genre_list

save_name = f"{filename}_summary.csv"
if save_name in os.listdir():
    previous = pd.read_csv(save_name)
    data = pd.concat([previous, data])
data.to_csv(save_name, index=False, encoding='utf-8-sig')