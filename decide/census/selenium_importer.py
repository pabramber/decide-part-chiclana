from pyexpat import model
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase
from voting.models import Question, Voting

class ImportTestCase(StaticLiveServerTestCase):

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
    
    def test_importWrongFormat(self):
        self.driver.get("http://127.0.0.1:8000/census/")
        self.driver.set_window_size(1299, 713)
        self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(4) .card-title").click()
        self.driver.find_element(By.NAME, "myfile").click()
        self.driver.find_element(By.NAME, "myfile").send_keys("C:\\fakepath\\census_formato_incorrecto.ods")
        #self.driver.find_element(By.CSS_SELECTOR, ".input-group-text:nth-child(4)").click()

        #messages = list(get_messages(response.wsgi_request))
        #self.assertEqual(len(messages), 'incorrect format, must be .xlsx')
        self.assertFalse(str(self.driver.find_elements(By.NAME,'myfile')), '')