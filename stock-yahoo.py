
# from datetime import datetime
# from threading import Timer

# x=datetime.today()
# y=x.replace(day=x.day, hour=22, minute=22, second=0, microsecond=0)
# delta_t=y-x

# secs=delta_t.seconds+1

def  task():	
	from selenium import webdriver
	from selenium.webdriver.support.ui import WebDriverWait
	import time
	import os
	import shutil

	#to delete the exiting folder having old datasets
	dir_path = '/Users/pranavsaxena/Desktop/Python/Dissertation-Datasets'

	try:
	    shutil.rmtree(dir_path)
	except OSError as e:
	    print("Error: %s : %s" % (dir_path, e.strerror))	
		
	#to connect to the Chromedriver
	options = webdriver.ChromeOptions() 
	pref = {'download.default_directory':'/Users/pranavsaxena/Desktop/Python/Dissertation-Datasets'}
	options.add_experimental_option("prefs",pref)
	options.add_experimental_option("excludeSwitches", ['enable-automation'])
	driver = webdriver.Chrome(chrome_options=options, executable_path='/Users/pranavsaxena/Desktop/Python/chromedriver')

	#Urls to be used to get the data
	uber_url = 'https://finance.yahoo.com/quote/UBER/history?p=UBER'
	accenture_url = 'https://finance.yahoo.com/quote/ACN/history?p=ACN'
	amazon_url = 'https://finance.yahoo.com/quote/AMZN/history?p=AMZN'
	dell_url = 'https://finance.yahoo.com/quote/DELL/history?p=DELL'
	apple_url = 'https://finance.yahoo.com/quote/AAPL/history?p=AAPL'
	verizon_url = 'https://finance.yahoo.com/quote/VZ/history?p=VZ'
	cisco_url = 'https://finance.yahoo.com/quote/CSCO/history?p=CSCO'
	fb_url = 'https://finance.yahoo.com/quote/FB/history?p=FB'

	url_list = [uber_url,accenture_url,amazon_url,dell_url,apple_url,verizon_url,cisco_url,fb_url]

	date = "//span[contains(@class,'C($linkColor) Fz(14px)')]"
	max_min_date = "//span[contains(text(),'Max')]"
	apply_filter = "//button[contains(@class,'Py(9px) Fl(end)')]"
	download = "//span[contains(text(),'Download')]"
	first_url= 'yes'

	for url in url_list:

		time.sleep(2)
		driver.get(url)
		if first_url == 'yes':
			button_element = WebDriverWait(driver,15).until(lambda driver: driver.find_element_by_name('agree'))
			button_element.click()

		button_element1 = WebDriverWait(driver,20).until(lambda driver: driver.find_element_by_xpath(date)) 
		button_element1.click()	
		button_element2 = WebDriverWait(driver,20).until(lambda driver: driver.find_element_by_xpath(max_min_date)) 
		button_element2.click()
		button_element3 = WebDriverWait(driver,20).until(lambda driver: driver.find_element_by_xpath(apply_filter)) 
		button_element3.click()	
		button_element4 = WebDriverWait(driver,5).until(lambda driver: driver.find_element_by_xpath(download))
		button_element4.click()

		first_url = 'no'

	time.sleep(2)
	driver.close()

task()

# t = Timer(secs, task)
# t.start()

