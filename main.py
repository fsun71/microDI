#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A simpler way of approaching DI- OTF made easy
"""
#Import necessary libraries and miscellaenous modules
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import time
import datetime

import numpy as np
import PySimpleGUI as sg
import timer

#Intializes variables for later use
usernames=[]
passwords=[]
names=[]
currentDT = datetime.datetime.now()
action=0

#Sets passtype to be weekend and return time to be 2300 if the current day is a Saturday or Sunday.
if currentDT.weekday()==5 or currentDT.weekday()==6:
	stype="Weekend"
	rtime=2300
#Otherwise, the return time is 1900 with a discretionary pass.
else:
	stype="Discretionary (Sponsor/SAP/VCS)"
	pass_comment="CompSci 212 Final Project test"
	rtime=1900

#Sets default location in case no changes to pass information are made by the user
location="Colorado Springs"
city="Colorado Springs"
state="Colorado"
rdate=str(currentDT.strftime("%m/%d/%y"))
retdate=str(currentDT.strftime("%Y-%m-%d"))

#Enables browser automation to function
browser = webdriver.Chrome()

#Retrieves information from data storage files; Usernames, Passwords, Names, Squads, and GPS Coordinates
with open("uns.txt", "r") as file:
    usernames = np.append(usernames,eval(file.readline()))
with open("pws.txt", "r") as file:
    passwords = np.append(passwords,eval(file.readline()))
with open("names.txt", "r") as file:
    names = np.append(names,eval(file.readline()))

#Logs the user into GoodForDI. Draws the ith instance from an array for each respectively field entry.
def login(i):
	browser.get('https://goodfordi.com/login')
	username = browser.find_element_by_name('email')
	username.send_keys(usernames[i])
	password = browser.find_element_by_name('password')
	password.send_keys(passwords[i])
	nextButton = browser.find_element_by_name('login')
	nextButton.click()

#Signs the users Form1 automatically. Draws the ith instance from an array for each respectively field entry.
def form1(i):
	signatures=names
	browser.get('https://goodfordi.com/form1')
	f1 = browser.find_element_by_name('signature')
	f1.send_keys(signatures[i])
	sign=browser.find_element_by_name('submit')
	sign.click()
	browser.get('https://goodfordi.com/logout')

#Signs the user out from USAFA on GoodForDI using user set pass information (or default value above). 
#Draws the ith instance from an array for each respectively field entry.
def signout():
	loc = browser.find_element_by_name('location')
	loc.send_keys(location)
	c=browser.find_element_by_name('city')
	c.clear()
	c.send_keys(city)
	drpState=Select(browser.find_element_by_name('state'))
	drpState.select_by_visible_text(state)

	nextPage=browser.find_element_by_xpath("//div[@id='wizard']/ul/li[2]/a")
	nextPage.click()
	time.sleep(0.5)

	signtype=Select(browser.find_element_by_name('signout_type'))
	signtype.select_by_visible_text(stype)
	retDate = browser.find_element_by_name('planned_return_date')
	retDate.send_keys(retdate)
	retTime = browser.find_element_by_name('planned_return_time')
	retTime.send_keys(rtime)
	nextPage.click()
	time.sleep(0.5)

	if(stype=='Discretionary (Sponsor/SAP/VCS)'):
		pcom = browser.find_element_by_name('pass_comments')
		pcom.send_keys(pass_comment)
		reason=Select(browser.find_element_by_name('disc_type'))
		reason.select_by_visible_text('AOC/AMT Authorized')

	if(stype=='SCA'):
		pcom = browser.find_element_by_name('sca_number')
		pcom.send_keys(sca_num)
	
	nextPage.click()
	time.sleep(0.5)

	sOut=browser.find_element_by_name('signout_button')
	sOut.click()

	browser.get('https://goodfordi.com/logout')

#Save function allows user to save all all relevant field information upon clicking any input button
def save():
	with open("uns.txt", "w") as file:
		file.write(str(list(usernames)))
	with open("pws.txt", "w") as file:
		file.write(str(list(passwords)))
	with open("names.txt", "w") as file:
		file.write(str(list(names)))

#Determines whether or not a user signs in or out
def actionFunc():
	if action==1:
		for i in np.arange(len(usernames)):
			login(i)
			signout()

	if action==2:
		for i in np.arange(len(usernames)):
			try:
				login(i)
				form1(i)
			except:
				sg.Popup("You have no more Form 1s to sign at this time.")
  

#Sets up Graphical User Interface using PySimpleGUI
layout = [	[sg.Button("Activate Daily Sign in", key="startTimer", tooltip="Click here to sign form 1 every 24 hours starting now."), 
			 sg.Button("Cancel Daily Sign in", key="stopTimer", tooltip="Click here to stop signing form 1 every 24 hours."),
			 sg.Button("Exit Program", key="exit")
			],

			[sg.Listbox(values=usernames,size=(72,4),key='userbox')],
			[sg.Listbox(values=passwords,size=(72,4),key='passbox')],
			[sg.Listbox(values=names,size=(72,4),key='namebox')],

			[
            	sg.Frame('',layout=[
            		[sg.T('Username:')], [sg.T('Password:    ')], [sg.T('Name:')]
            		]),
            	sg.Frame('',layout=[
            		[sg.Input(size=(52,4))], [sg.Input(size=(52,4))], [sg.Input(size=(52,4))]
            		])
            ],

            [
            	sg.RButton('Add Account',key='add'),
				sg.RButton("Remove Last Account",key='remove'),
            ],

			[
				sg.Frame('',font="Arial",layout=[
					[sg.T("Pass Type:")],
					[sg.T("City")],
					[sg.T("State")],
					[sg.T("Return Time")],
					[sg.T("Return Date")],
					[sg.T("Comments")],
					[sg.T("SCA Number")]
				]),
            	sg.Frame('',layout=[
            		[sg.InputCombo(['Weekend','Discretionary (Sponsor/SAP/VCS)', 'ACQ','TAPS','SCA'],key='passtype',size=(49,4))], 
            		[sg.Input("Colorado Springs",size=(52,4))],
            		[sg.Input("Colorado",size=(52,4))],
            		[sg.Input("1900",size=(52,4))], 
            		[sg.Input(str(currentDT.strftime("%Y-%m-%d")),size=(52,4))],
            		[sg.Input(size=(52,4))],
            		[sg.Input(size=(52,4))]
            		])
			],

			[
				sg.Button('Sign out now!', key='signout'),
				sg.Button('Sign in now!',key='signin'),
				sg.RButton("Set Pass Info",key='passInfo'),
				sg.RButton("View Current Pass Info",key='viewInfo')
			]
		]

window = sg.Window('MicroG4DI', icon="eye.ico").Layout(layout) 

#Event loop that gives each button functionality and allows user inputted information to be raed in
while True:  
	event, values = window.Read()

	#Immediately signs the user out in GoodForDI
	if event == 'signout':
		action=1
		actionFunc()
		save()

	#Immediately signs the user in to GoodForDI
	if event == 'signin':
		action=2
		actionFunc()
		save()

	#Adds a new user and saves all relevant information; updates displayed information
	if event == 'add':
		if values[0]!="" and values[1]!="" and values[2]!="" and values[3]!="":
			usernames = np.append(usernames,values[0])
			passwords = np.append(passwords,values[1])
			names = np.append(names,values[2])
			signatures=names
			save()

			window.FindElement('userbox').Update(values=usernames)
			window.FindElement('passbox').Update(values=passwords)
			window.FindElement('namebox').Update(values=names)

		else:
			sg.Popup("Error: One or more of the above fields were left empty")
	
	#Removes the most recently added account; updates displayed information
	if event == 'remove':
		try:
			usernames=np.delete(usernames,-1)
			passwords=np.delete(passwords,-1)
			names=np.delete(names,-1)
			signatures=names
			save()

			window.FindElement('userbox').Update(values=usernames)
			window.FindElement('passbox').Update(values=passwords)
			window.FindElement('namebox').Update(values=names)

		#Accounts for attempting to remove accounts when there are no accounts left
		except IndexError:
			sg.Popup("Error: There are currently no accounts on record.")

	#Sets up daily form1 loop, signs them in immediately and then repeatedly signs them in every 24 hours (86400 seconds)
	if event == 'startTimer' or event == 'stopTimer':
		action=2
		t=timer.perpetualTimer(86400, actionFunc)

		if event == 'startTimer':
			sg.Popup("Will sign in again at this time tomorrow")
			actionFunc()
			t.start()

		if event == 'stopTimer':
			sg.Popup("Timer stopped")
			t.cancel()

	#Reads in user inputted pass information
	if event == 'passInfo':
		stype=values['passtype']
		city=values[4]
		location=values[4]
		state=values[5]
		rdate=values[6]
		rtime=values[7]
		pass_comment=values[8]
		sca_num=values[9]

		sg.Popup("Pass information set.")
		save()

	#Allows user to view all inputted information
	if event == "viewInfo":
		sg.Popup(stype,city,location,state,rdate,rtime, grab_anywhere=True)
		
	#Exits program
	if event =='exit':
		break






