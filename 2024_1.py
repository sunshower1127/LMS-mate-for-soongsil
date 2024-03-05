from driver import Element, conditions
import time
from datetime import datetime

with open('idpw.txt', 'r', encoding='utf-8') as file :
    id = file.readline().strip()
    pw = file.readline().strip()

with open('ban.txt', 'r', encoding='utf-8') as file :
    ban_list = file.read()


driver = Element()

driver.url('https://lms.ssu.ac.kr/login')

driver.find(name='userid').send_keys(id)
driver.find(name='pwd').send_keys(pw)
driver.find(text='로그인').click()
driver.find(text='마이페이지').parent().click()

driver.iframe()
subjects = driver.find_all(raw='//' + conditions(tag='span', classes='xntc-title', text='동영상') + \
                           '/../' + conditions(tag='a', text='>0'))

