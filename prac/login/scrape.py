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

wrong_url = r'http://app.myvitbhopal.ac.in/corecampus/index.php?errormessage=Invalid+Username+or+Password.Please+try+again.'

#----selenium
cookie = []
#------/selenium

path = os.path.dirname(os.path.realpath(__file__))+'/chromedriver'
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
	driver.find_element_by_class_name('btn_img').click()


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
	for i in matter.findAll('td'):
		if count ==0:
			string['id']=i.text
		elif count == 1:
			string['code']=i.text
		elif count == 2:
			string['subject']=i.text
		elif count == 3:
			string['credit']=i.text
		elif count == 4:
			string['total']=i.text
		elif count == 5:
			string['percent']=i.text
		elif count == 6:
			string['useless']=i.text
		count+=1
		if count==7:
			lis.append(string.copy())
			count=0
	driver.close()
	return {"lis":lis,"name":name}




if __name__=="__main__":
	feedback()
