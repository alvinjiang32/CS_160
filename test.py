from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class ContactUsFormTest(LiveServerTestCase):

  def test_form(self):
    # Arrange
    selenium = webdriver.Firefox()
    selenium.get('http://127.0.0.1:8000/contact')
    name = selenium.find_element_by_id('firstname')
    email = selenium.find_element_by_id('email')
    subject = selenium.find_element_by_id('data')
    submit = selenium.find_element_by_class_name("btn-outline-info")

    time.sleep(1) # For gif capturing

    # Action
    name.send_keys('Sam Vuong')
    time.sleep(1)
    email.send_keys('rec_sports@gmail.com')
    time.sleep(1)
    subject.send_keys('I would like to cancel my reservation.')
    time.sleep(1)
    submit.send_keys(Keys.RETURN)
    time.sleep(1)

    # Assert
    assert 'Thank you Sam Vuong, we will be contact with you shortly!' in selenium.page_source