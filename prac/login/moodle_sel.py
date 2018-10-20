from selenium import webdriver
from bs4 import BeautifulSoup 
from selenium.webdriver.support.ui import Select, WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import os
import json
cookie =[]
def moodle(username, password):
	global cookie
	opt = webdriver.ChromeOptions()
	opt.add_argument("--incognito")
	prefs = {"profile.managed_default_content_settings.stylesheet":2,"Javascript.enabled": False}
	opt.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome(options=opt)
	driver.get('http://moodle.vitbhopal.ac.in/login/index.php')
	url= driver.current_url
	driver.find_element_by_name('username').send_keys(username)
	driver.find_element_by_name('password').send_keys(password)
	driver.find_element_by_id('loginbtn').click()
	if url==driver.current_url:
		return "failed"
	
	cookie = driver.get_cookies()
	pickle.dump(driver.get_cookies(), open(os.path.join("login/data/")+username+"_cook_mood.pkl", "wb"))
	events = []
	soup = BeautifulSoup(driver.page_source, 'html.parser')

	user = soup.findAll('span' , {"class" : "usertext"})
	temp = []
	temp1 = []
	link=[]
	links = []
	text = []
	date= []
	seven_days = soup.findAll('li', {"class":"list-group-item event-list-item"})
	event = soup.findAll('div', {"class" : "event"})
	for i in event:
		temp.append(i.text.replace("_"," "))
		temp1.append(str(i.a['href']))
	isimp = "YES"

	if (not temp) or (not temp1):
		isEvent="NO"
	else:
		isEvent="YES"
	calendar = soup.findAll('table', {"class" : "minicalendar calendartable"})
	in_this_month = soup.findAll('td' , {"class" : "day hasevent calendar_event_course calendar_event_course"})


	for i in in_this_month:
		date.append(i.a['data-title'])
		s = BeautifulSoup(str(i.a['data-content']),'html.parser')
		link.append(s.findAll('a'))
	for i in link:
		for j in i:
			text.append(j.text.replace("_"," "))
			links.append(str(j['href']))
	if not text:
		isimp="NO"
	driver.close()
	
	return {'events':isEvent, 'text' : text,'links' : links, 'date' : date, 'temp' : temp,'temp1' : temp1 , 'name' : user[0].text.split(" ")[0].capitalize(), 'isimp':isimp}
def assign(string, user , passw):
	opt = webdriver.ChromeOptions()
	opt.add_argument("--incognito")
	prefs = {"profile.managed_default_content_settings.stylesheet":2}
	opt.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome(options=opt)
	driver.get(string)
	url= driver.current_url
	driver.find_element_by_name('username').send_keys(user)
	driver.find_element_by_name('password').send_keys(passw )
	driver.find_element_by_id('loginbtn').click()
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	table = soup.find('table',{"class","generaltable"})
	oldleftSide = table.findAll('td',{'class':"c0"})
	oldrightSide = table.findAll('td',{'class':'lastcol'})
	leftSide=[]
	rightSide=[]
	for i in oldleftSide[:4]:
		leftSide.append(i.text)
	
	
	for i in oldrightSide[:4]:
		rightSide.append(i.text)
	
	driver.close()
	return {"leftSide":leftSide,"rightSide":rightSide}




