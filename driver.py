from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from functools import wraps

def sleep(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        time.sleep(0.1)
        return result

    return wrapper

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



class Element :
    def __init__(self, element=driver) :
        self.current_element = element

    @sleep
    def url(self, url) :
        driver.get(url)
    
    
    def find(self, raw=None, tag='*', **kwargs) :
        '''
        id, name, classes, position, text, and other props
        '''
        if raw :
            return Element(self.current_element.find_element(By.XPATH, raw))
        else :
            return Element(self.current_element.find_element(By.XPATH, '//' + conditions(tag, **kwargs)))


    def find_all(self, raw=None, tag='*', **kwargs) :
        '''
        id, name, classes, position, text, and other props
        '''
        if raw :
            return [Element(element) for element in self.current_element.find_elements(By.XPATH, raw)]

        else :
            return [Element(element) for element in self.current_element.find_elements(By.XPATH, '//' + conditions(tag, **kwargs))]


    @sleep
    def click(self) :
        self.current_element.click()
    
    @sleep
    def send_keys(self, *args) :
        self.current_element.send_keys(args)

    def iframe(self) :
        driver.switch_to.frame(self.current_element.find_element(By.XPATH, '//' + conditions(tag='iframe')))

    def parent(self) :
        return Element(self.find(raw='../'))
    
    def text(self) :
        return self.current_element.text