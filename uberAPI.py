from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlwings as xw
import time,pyperclip, pyautogui as p 
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

#install latest Chrome drivers for selenium
browser = webdriver.Chrome(ChromeDriverManager().install())
#Go to uber login page 
browser.get('https://auth.uber.com/login/#_')

#LOCATIONS
file_dest_loc = 'D:\\Drive\\OneDrive\\Uber\\dest115.txt'
file_pickup_loc = 'D:\\Drive\\OneDrive\\Uber\\pickuppoints115.txt'
file_excel_loc = 'D:\\test.xlsx'
name_sheet = 'Sheet1'

#Read destlination and pick up points files
dest = open(file_dest_loc,'r', encoding = 'utf8')
pp = open(file_pickup_loc, 'r', encoding='utf8')

#Pick up points and destination points lists  
pp_list = pp.readlines()
dest_list = dest.readlines()

#Load Excel file and sheet
wb = xw.Book(file_excel_loc)
sheet = wb.sheets[name_sheet]
#Count number of rows we already have in the file
rows = pd.read_excel(file_excel_loc)

#Function to find any element in the browser with its xpath and set its value in case of input field
#defined by the input_filed parameter( TRUE) and value using value parameter
def findAndSetValue(xpath, input_field, value = None):
    time.sleep(2) #waits for 2 second so that page can load 
    try:
        element = browser.find_element_by_xpath(xpath)
        time.sleep(2) 
        element.click()
        if input_field:
            element.send_keys(value) #Sets value ( insert into input box)
            return element
    except: #In case no such element found skip the calls 
        pass
#Functino to get the text value visible on screen using its xpath
def getValue(xpath):
    try:    
        time.sleep(4)
        element = browser.find_element_by_xpath(xpath).text #Get the text value 
        return element
    except: #in case no such element found return a None value
        element=None

url=("https://m.uber.com/looking?_ga=2.91551898.1074888867.1610477863-92334322.1610477863&uclick_id=4fbeb21f-9daa-4579-8f3b-74a3b382165d")
pyperclip.copy(url)
input("Continue")

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


#Set the headers for the excel sheet     
sheet.range('A1').value = "Pickup points"
sheet.range('B1').value = "Destination points"
sheet.range('C1').value = "Price"
#Get the latest row feeded by the bot and add 2 (1 for headers and 1 for as index of array starts from 0)
start = max(rows.index)+2
end = 115 #Total number of pickup and destination points we have 

for count, i in enumerate(range(start,end)):

    findAndSetValue(xpath[0], True, pp_list[i])#Find pick up point and click on it 
    findAndSetValue(xpath[1], False)#Select first element from the list of pick up points
    findAndSetValue(xpath[2], True, dest_list[i])#Find destination point and click on it 
    findAndSetValue(xpath[3], False)#Select first element from the list of destination points
    #Wait for 3 seconds to let the page loads its data completely
    time.sleep(3)
    #Get the text values of actually selected pick up and destination point's values for confirmation
    #and Feed into excel sheet
    sheet.range('A'+str(i+1)).value = getValue(pick).split(' ', 1)[1]
    sheet.range('B'+str(i+1)).value = getValue(dest).split(' ', 1)[1]
    price = getValue(prrice) #Get the ubergo Price provided by the website
    sheet.range('C'+str(i+1)).value = float(str(price)[1:]) #Feed price value in excel
    wb.save() #Save the workbook till now for backup in case code stops working somewhere
    if price is None:
        if count > 59:
            time.sleep(1200)
        else:
            time.sleep(15)
    browser.back()
    browser.back()





