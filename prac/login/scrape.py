import mechanicalsoup
import getpass
import re
import random
import pickle
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from sys import platform
import time
wrong_url = r'http://app.myvitbhopal.ac.in/corecampus/index.php?errormessage=Invalid+Username+or+Password.Please+try+again.'

#----selenium
cookie = []
#------/selenium
if platform=="linux" or platform=="linux2":
	path = os.path.dirname(os.path.realpath(__file__))+'/chromedriver_linux64/chromedriver'
elif platform=="win32":
	path = 	path = os.path.dirname(os.path.realpath(__file__))+'/chromedriver_win32/chromedriver.exe'
elif platform=='darwin':
	path = os.path.dirname(os.path.realpath(__file__))+'/chromedriver_mac64/chromedriver'


def feedback():
	br.set_cookiejar(cookie)
	br.open("http://app.myvitbhopal.ac.in/corecampus/student/subjects/mycontents.php")
	soup = br.get_current_page()
	matter = soup.findAll('a',{'href' : re.compile('^teachplan_rating.php')})
	br.open('http://app.myvitbhopal.ac.in/corecampus/student/subjects/'+matter[0]['href'])
	soup = br.get_current_page()
	button = soup.find('input', {'id' : re.compile('rat_a\d')})
	form = br.select_form()
	br['rat_16']="5"
	br['cmt_16']="Good"
	form.choose_submit(soup.find({'ng-click':'sub_form("16")'}))
	br.submit(form)
	br.launch_browser()


def attendance(username,password):
	global cookie
	opt = webdriver.ChromeOptions()
	opt.add_argument("--incognito")

	prefs = {"profile.managed_default_content_settings.images":2,"profile.managed_default_content_settings.stylesheet":2}
	opt.add_experimental_option("prefs",prefs)

	driver = webdriver.Chrome(executable_path=path,options=opt)
	cookie = driver.get_cookies()

	driver.get('http://app.myvitbhopal.ac.in/corecampus/index.php')
	if "ERR_EMPTY_RESPONSE" in driver.page_source:
		driver.refresh()
	soup = BeautifulSoup(driver.page_source, 'html.parser')

	if soup.find('div', {"class":"error-code"}) :
		return "Error code"
	driver.find_element_by_name('userid').send_keys(username)
	driver.find_element_by_name('pass_word').send_keys(password)
	driver.find_element_by_css_selector('button[value="Submit"]').click()


	try:
		driver.get('http://app.myvitbhopal.ac.in/corecampus/student/topfr.php')
	except UnexpectedAlertPresentException:
		alert = driver.switch_to_alert()
		alert.accept()
	soup1 = BeautifulSoup(driver.page_source, 'html.parser')
	name = soup1.find('span',{"class":"userclass"}).text.split(' ')[0]

	if driver.current_url == wrong_url:
		return "Wrong Credentials!"
	try:
		driver.get("http://app.myvitbhopal.ac.in/corecampus/student/attendance/subwise_attendace.php")

	except UnexpectedAlertPresentException:
		alert = driver.switch_to_alert()
		alert.accept()
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	matter = soup.find('table',{'id' : 'ReportTable'})

	lis = list()
	count=0
	string={}
	index_list = []
	columns = ["Sr.No", "Course Code", "Course Title", "Course Credit",
	 "Total Attended/Total Conducted", "Percentage"]
	column = ["id", "code", "subject", "credit", "total","percent"]
	headings = matter.findAll('th')

	for i in range(len(headings)):
		if headings[i].text in columns:
			index_list.append(i)
	print(index_list)
	table = matter.findAll('tr')[1:]
	for j in table:
		li = j.findAll('td')
		print(li)
		index = 0
		for i in index_list:
			string[column[index]] = li[i].text
			index+=1
		lis.append(string.copy())
	driver.close()
	print(lis, index_list)
	return {"lis":lis,"name":name}

def verify(username, password):
		opt = webdriver.ChromeOptions()
		opt.add_argument("--incognito")
		prefs = {"profile.managed_default_content_settings.images":2,"profile.managed_default_content_settings.stylesheet":2}
		opt.add_experimental_option("prefs",prefs)

		driver = webdriver.Chrome(executable_path=path,options=opt)
		cookie = driver.get_cookies()

		driver.get('http://app.myvitbhopal.ac.in/corecampus/index.php')
		if "ERR_EMPTY_RESPONSE" in driver.page_source:
			driver.refresh()
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		url =driver.current_url

		driver.find_element_by_name('userid').send_keys(username)
		driver.find_element_by_name('pass_word').send_keys(password)
		driver.find_element_by_class_name('btn_img').click()
		try :
			if url==driver.current_url:
				driver.close()

				return False
			else:
				driver.close()

				return True
		except:
			driver.switch_to_alert().accept()
			return False

if __name__=="__main__":
	print(verify('17bce10023',''))
