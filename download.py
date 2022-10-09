import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

PAGES = 320 #书的总页数
ADDRESS = 'https://wqbook.wqxuetang.com/read/pdf?bid=3236039' #书的网址
driver = webdriver.Chrome('C:\\src\\webdriver\\chromedriver.exe') #括号内写你的chromedriver.exe所在的位置

def wechat_signin(driver, wait_time=60):
    '''
    wait_time: how long the driver waits at the QR code scanning page
    '''
    signin = driver.find_element(by=By.XPATH, value='//*[@id="app"]/header/div[2]/span[2]')
    signin.click()
    time.sleep(1)

    wechat = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-login/div/div/div[2]/div[3]/div[2]/img[1]')
    wechat.click()
    time.sleep(wait_time)

def go_to_page_n(driver, n):
    '''
    使用鼠标滚轮跳转到对应页数。
    '''
    ActionChains(driver)\
        .scroll_to_element(pages[n])\
        .perform()

def right_click_save_as(segment):
    '''
    segment: 我们想另存为所对应的<img>
    '''
    ActionChains(driver)\
        .context_click(segment)\
        .perform()

    pyautogui.typewrite(['down', 'down', 'enter', 'enter'], interval=0.5) #键盘输入下，下，回车，回车
    time.sleep(0.5)


# driver.maximize_window() #将浏览器窗口最大化
driver.get(ADDRESS)
time.sleep(1)

wechat_signin(driver)

# 获取书名
title = driver.find_element(by=By.CLASS_NAME, value='page-head-s').text
print(title)

# 获取高清图片
pages = driver.find_elements(by=By.CLASS_NAME, value='page-img-box')

for page in range(1, PAGES + 1):
    go_to_page_n(driver, page)
    time.sleep(5) # 翻页后，给高清图片加载预留时间

    # 将每一个细分图片找到，统一存在pieces这个list里
    img = pages[page].find_element(by=By.CLASS_NAME, value='page-lmg')
    pieces = img.find_elements(by=By.TAG_NAME, value='img')

    # 根据“left"的css值来排序
    order = []
    row = []
    for piece in pieces:
        row.append(float(piece.value_of_css_property('left')[:-2]))

    while len(order) != len(row):
        for n in range(len(row)):
            if n not in order:
                mini = row[n]

        i = 0
        while i < len(row):
            if row[i] < mini and i not in order:
                mini = row[i]
            i += 1
        # 找到最小
        order.append(row.index(mini))
    
    for e in order:
        right_click_save_as(pieces[e])

driver.quit()