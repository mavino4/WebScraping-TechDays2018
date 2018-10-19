from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display
import time
import urllib
import os

# Para poder observar la pantalla virtual cambie el parámetro visible = 1
xephyr=Display(visible=1, size=(320, 240)).start()

# Las variables que ingresan son strings, a excepción del
# parámetro j, que en este caso es el contador
def sendTigo(name,Tigo,Mensaje,j):
	driver = webdriver.Chrome()
	driver.get('http://www.bolivia-sms.com/tigo.html')
	driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))


	Alias = driver.find_element_by_id("nickname")
	Alias.click()
	Alias.clear()
	for i in name:
	    Alias.send_keys(i)


	select1 = Select(driver.find_element_by_id('carea'))
	select1.select_by_value(Tigo[:2])


	number = driver.find_element_by_id('celnum')
	number.click()
	for i in Tigo[2:]:
	    number.send_keys(i)


	msg = driver.find_element_by_id('message')
	msg.click()
	for i in Mensaje:
	    msg.send_keys(i)


	send = False
	while ( not send):
		try:
			number = driver.find_element_by_id('celnum')
			number.click()
			msg = driver.find_element_by_id('message')
			msg.click()
			time.sleep(2)
			image = driver.get_screenshot_as_png()
			file = open("screenshoot.png" ,"wb")
			file.write(image)

			os.system("python3 resize.py")
			os.system("python3 solve_captchas.py")	

			captcha = open("solution.txt",'r')
			solution = captcha.readline()
			textcode = driver.find_element_by_id('textcode')
			textcode.click()
			textcode.clear()
			for i in solution:
			    textcode.send_keys(i)
			captcha.close()

			msg = driver.find_element_by_id('submit')
			msg.click()

			os.system("rm -f screenshoot.png")
			os.system("mv -f test_i/test.png solved/%s.png" % (solution))
			time.sleep(3)
			sendTigo = driver.find_element_by_id('mensajesRecibidos')
			print("Esto va a la salida de texto")
			# El mensaje que efectivamente se envío
			print(sendTigo.text)
			if len(sendTigo.text)> 0: 
				send = True
		except: 
			alert = driver.switch_to_alert()
			alert.accept()
			os.system("mv -f solved/%s.png failed/%s.png" % (solution,solution))
	driver.close()

name = ["CCD-LP"]*2
Tigo = ["77579235"]*2
mensaje = ["Únete http://bit.ly/ccdlp"]*2

for k in range(len(name)):
	sendTigo(name[k],Tigo[k],mensaje[k],k)
