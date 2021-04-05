from selenium import webdriver
import time, pyautogui as p 
browser = webdriver.Chrome(executable_path='D:\\Drive\\OneDrive\\Uber\\chromedriver.exe')
browser.get('https://auth.uber.com/login/#_')

dest = open('D:\\Drive\\OneDrive\\Uber\\dest.txt','r', encoding = 'utf8')
pp = open('D:\\Drive\\OneDrive\\Uber\\pickuppoints.txt', 'r', encoding='utf8')



pp_list = pp.readlines()
dest_list = dest.readlines()
desti = []
pps = []


def findAndSetValue(xpath, input_field, value = None):
    try:
        element = browser.find_element_by_xpath(xpath)
        time.sleep(2)
        element.click()
        if input_field:
            element.send_keys(value)
    except:
        findAndSetValue(xpath, input_field, value)

def getValue(xpath):
    try:
        time.sleep(2)
        element = browser.find_element_by_xpath(xpath).text
        if element is None:
            getValue(xpath)
        return element
    except:
        getValue(xpath)

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
    'https://m.uber.com/looking?_ga=2.91551898.1074888867.1610477863-92334322.1610477863&uclick_id=4fbeb21f-9daa-4579-8f3b-74a3b382165d'
]

login(logins[0], True, 'UserID')
login(logins[1], False)
login(logins[2], True, 'password')


input("Continue")

xpath=[
    '//*[@id="booking-experience-container"]/div/div[3]/div[2]/div/div/div[1]/div/input',#pickup_point
    '//*[@id="booking-experience-container"]/div/div[3]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[1]',#pickup_click
    '//*[@id="booking-experience-container"]/div/div[3]/div[2]/div/div/div[1]/div/input',#des_point
    '//*[@id="booking-experience-container"]/div/div[3]/div[2]/div/div/div[2]/div/div[1]/div[2]',#des_click
    '/html/body/div[1]/div[2]/div[2]/div/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/span/p'#price
]




for i in range(9,83):
    result_file = open('D:\\Drive\\OneDrive\\Uber\\aiport-14-2021.txt', 'a')
    findAndSetValue(xpath[0], True, pp_list[i])#pickuppoint 
    findAndSetValue(xpath[1], False)#select_pickup_point
    findAndSetValue(xpath[2], True, dest_list[i])#dest_point
    findAndSetValue(xpath[3], False)#select_dest_point
    time.sleep(3)
    price = getValue('//*[@id="booking-experience-container"]/div/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/span/p[2]')#get price
    print(price)
    result_file.write(str(i+1)+"="+price[1:-1]+"\n")
    browser.back()
    browser.back()
    result_file.close()

