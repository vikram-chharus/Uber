#import pandas as pd
from typing import Counter
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
browser = webdriver.Chrome(ChromeDriverManager().install())
import xlwings as xw
import time,pyperclip, pyautogui as p 
# from playsound import playsound
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

#browser = webdriver.Chrome(executable_path='C:\\Users\\Lenovo\\Downloads\\uber_code\\chromedriver.exe')
browser.get('https://auth.uber.com/login/#_')

dest = open('D:\\Drive\\OneDrive\\Uber\\dest115.txt','r', encoding = 'utf8')
pp = open('D:\\Drive\\OneDrive\\Uber\\pickuppoints115.txt', 'r', encoding='utf8')
#file=pd.read_excel(r'D:\STUFF\uber_code\test.xlsx')
  
pp_list = pp.readlines()
dest_list = dest.readlines()
desti = []
pps = []

xl_loc = 'D:\\test.xlsx'
wb = xw.Book(xl_loc)
sheet = wb.sheets['Sheet1']

rows = pd.read_excel(xl_loc)

def findAndSetValue(xpath, input_field, value = None):
    time.sleep(2)
    try:
        element = browser.find_element_by_xpath(xpath)
        time.sleep(2)
        element.click()
        if input_field:
            element.send_keys(value)
            return element
    except:
        #findAndSetValue(xpath, input_field, value)
        pass

def getValue(xpath):
    try:    
        time.sleep(4)
        element = browser.find_element_by_xpath(xpath).text
        return element
    except:
        element=None

    

def login(xpath, input_field, value = None):
    try:
        element = browser.find_element_by_xpath(xpath)
        element.click()
        if input_field:
            element.send_keys(value)
    except:
        findAndSetValue(xpath, input_field, value)
        
logins = [
    '//*[@id="useridInput"]',
    '//*[@id="app-body"]/div/div[1]/form/div[2]/button',
    '//*[@id="password"]',
    '//*[@id="app-body"]/div/div[1]/form/div[2]/button',
    'https://m.uber.com/looking?_ga=2.91551898.1074888867.1610477863-92334322.1610477863&uclick_id=4fbeb21f-9daa-4579-8f3b-74a3b382165d'
]

#login(logins[0], True, '8882023736')
#login(logins[1], False)
#login(logins[2], True,"uber@1234")

url=("https://m.uber.com/looking?_ga=2.91551898.1074888867.1610477863-92334322.1610477863&uclick_id=4fbeb21f-9daa-4579-8f3b-74a3b382165d")
#pyperclip.copy('uber@1234')
pyperclip.copy(url)
input("Continue")
#time.sleep(2)


xpath=[
    '//*[@id="booking-experience-container"]/div/div[3]/div[2]/div/input',#pickup_point
    '//*[@id="booking-experience-container"]/div/div[3]/div[4]/div/div[2]/div[1]',#pickup_click
    '//*[@id="booking-experience-container"]/div/div[3]/div[2]/div/input',#des_point
    '//*[@id="booking-experience-container"]/div/div[3]/div[4]/div[1]/div[2]/div[1]',#des_click
    '//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[4]/div/div[2]/div[1]/div/span[1]',#premier
    '//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[6]/div/div[2]/div[1]/div/span[1]',#ubergo rentals
    '//*[@id="booking-experience-container"]/div[2]/div[1]'#back
]
normal_price='//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[1]/div/div[3]/div/span/p'
discount_price='//*[@id="booking-experience-container"]/div/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/span/p[2]'
premiere='//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[5]/div/div[2]/div[1]/div/span[1]'
ubergo_rentals='//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[6]/div/div[2]/div[1]/div/span[1]'
premier_price='//*[@id="booking-experience-container"]/div[2]/div[2]/div[2]/div[2]/h4'
ubergo_rentalsprice='//*[@id="booking-experience-container"]/div[2]/div[2]/div[2]/div[2]/h4'



pick='//*[@id="booking-experience-container"]/div/div[2]/div/div/div[1]/div[2]/div'
dest='//*[@id="booking-experience-container"]/div/div[2]/div/div[2]/div[2]/div[2]/div'

def pd(location):
    try:

        #s.range(column+str(i)).value = el
        el= browser.find_element_by_xpath(location).text
        el=el.split("Chevron")[0]
        return el
    except NoSuchElementException:
        pass 

    
    
sheet.range('A1').value = "Pickup points"
sheet.range('B1').value = "Destination points"
sheet.range('C1').value = "Price"
start = max(rows.index)+2
end = 115
prrice=normal_price
for count, i in enumerate(range(start,end)):
    findAndSetValue(xpath[0], True, pp_list[i])#pickuppoint
    findAndSetValue(xpath[1], False)#select_pickup_point
    findAndSetValue(xpath[2], True, dest_list[i])#dest_point
    findAndSetValue(xpath[3], False)#select_dest_point
    
    time.sleep(3)
    sheet.range('A'+str(i+1)).value = pd(pick).split(' ', 1)[1]
    sheet.range('B'+str(i+1)).value = pd(dest).split(' ', 1)[1]
    price = getValue(prrice)
    sheet.range('C'+str(i+1)).value = float(str(price)[1:])
    wb.save()
    if price is None:
        if count > 59:
            time.sleep(1200)
        else:
            time.sleep(15)

    print(str(i)+"="+str(price))
    browser.back()
    browser.back()





