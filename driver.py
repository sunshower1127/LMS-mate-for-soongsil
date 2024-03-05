from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from functools import wraps

import traceback

# def repeat(func) :
#     @wraps(func)
#     def wrapper(*args, **kwargs):

#         timeout = 20
        
#         for i in range(timeout) :
#             try:
#                 print(i)
#                 return func(*args, **kwargs)
#             except:
#                 time.sleep(1)
        
#         raise Exception('Repeat Error')
#     return wrapper


# def sleep(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         time.sleep(0.1)
#         return result

#     return wrapper

def conditions(tag, **kwargs) :
    result = tag

    if not kwargs :
        return result
     
    result += '['

    '''
    contains 분리하기.

    class a or b or c

    모든 tag에 and, or, contains
    <> 적용.
    
    and or contains
    
    '''

    for key, value in kwargs.items() :
        if result[-1] != '[' :
            result += ' and '
        
        if key == 'id' or key == 'name' :
            result += f'@{key}="{value}"'
            break
        
        elif key == 'classes' :
            
            if ' or ' in value :
                or_split = value.split(' or ')
                value = '(' + ' or '.join( f'contains(@class, "{name}")' for name in or_split ) + ')'
            
            elif ' and ' in value :
                or_split = value.split(' and ')
                value = '(' + ' and '.join( f'contains(@class, "{name}")' for name in or_split ) + ')'
            
            else :
                value = f'contains(@class, "{value}")'
            result += value
        
        elif key == 'position' :
            if value[0] == '<' or value[0] == '>' :
                result += f'position(){value}'
            else :
                result += f'position()={value}'
        
        elif key == 'text' :
            if value[0] == '<' or value[0] == '>' :
                result += f'number(text())' + value
            else : 
                result += f'text()="{value}"'
        
        else :
            result += f'@{key}="{value}"'

    result += ']'
    return result

chrome_options = webdriver.ChromeOptions()

chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--mute-audio")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 20)
class Element :
    def __init__(self, element=driver) :
        self.current_element = element

    
    def url(self, url) :
        driver.get(url)
    
    def find(self, raw=None, tag='*', **kwargs) :
        '''
        id, name, classes, position, text, and other props
        '''
        path = raw if raw else '//' + conditions(tag, **kwargs)
        
        wait.until(EC.presence_of_element_located((By.XPATH, path)))

        return Element(self.current_element.find_element(By.XPATH, path))


    def find_all(self, raw=None, tag='*', **kwargs) :
        '''
        id, name, classes, position, text, and other props
        '''

        path = raw if raw else '//' + conditions(tag, **kwargs)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, path)))

        return [Element(element) for element in self.current_element.find_elements(By.XPATH, path)]


    def click(self) :
        # wait.until(EC.element_to_be_clickable(self.current_element))
        self.current_element.click()
    
    def send_keys(self, *args) :
        self.current_element.send_keys(args)

    def iframe(self) :
        path = '//' + conditions(tag='iframe')
        driver.switch_to.frame(driver.find_element(By.XPATH, path))

    def parent(self) :
        return Element(self.current_element.find_element(By.XPATH, '../*'))
    
    def text(self) :
        return self.current_element.text
    
    def sleep(self, sec) :
        time.sleep(sec)
    