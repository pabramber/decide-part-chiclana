# Generated by Selenium IDE
import pytest
import time
import json
from .models import Census
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestFilterCensus():
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
  
  def test_filterCensus(self):
    self.driver.get("http://127.0.0.1:8000/census/")
    self.driver.set_window_size(930, 704)
    self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(7) .card-title").click()
    self.driver.find_element(By.NAME, "q").click()
    self.driver.find_element(By.NAME, "q").send_keys("Roger")
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(4) .input-group-text").click()
    self.driver.find_element(By.NAME, "i").click()
    self.driver.find_element(By.NAME, "i").send_keys("1")
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(2) .input-group-text").click()
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(7) .input-group-text").click()
    self.driver.find_element(By.CSS_SELECTOR, ".a2 > .card-body > .card-title").click()
    self.driver.find_element(By.CSS_SELECTOR, ".a2 > .card-body").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(4) .card-title").click()
    self.driver.find_element(By.NAME, "myfile").click()
    self.driver.find_element(By.NAME, "myfile").send_keys("C:\\fakepath\\Datos1.xlsx")
    self.driver.find_element(By.CSS_SELECTOR, "button").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(7) .card-title").click()
    self.driver.find_element(By.NAME, "q").click()
    self.driver.find_element(By.NAME, "q").send_keys("Roger")
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(4) .input-group-text").click()
    self.driver.find_element(By.NAME, "i").click()
    self.driver.find_element(By.NAME, "i").send_keys("1")
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(2) .input-group-text").click()
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(12) .form-control").click()
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(12) .form-control").send_keys("0")
    self.driver.find_element(By.CSS_SELECTOR, "form:nth-child(12) .input-group-text").click()
  
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
      c=Census.objects.all()
      self.assertEqual(Census.objects.count(), 0)

  #A??adimos un censo y comprobamos que se exporta correctamente
  def test_exporttest(self):
    
    self.driver.get("http://127.0.0.1:8000/census/")
    self.driver.set_window_size(1366, 685)
    self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(6) .card-title").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(1) .card-title").click()
    self.driver.find_element(By.ID, "id_voting_id").click()
    self.driver.find_element(By.ID, "id_voting_id").send_keys("2")
    self.driver.find_element(By.ID, "id_voter_id").send_keys("2")
    self.driver.find_element(By.ID, "id_name").send_keys("2")
    self.driver.find_element(By.ID, "id_surname").send_keys("2")
    self.driver.find_element(By.ID, "id_city").send_keys("2")
    self.driver.find_element(By.ID, "id_a_community").send_keys("2")
    self.driver.find_element(By.ID, "id_gender").send_keys("2")
    self.driver.find_element(By.ID, "id_born_year").send_keys("2")
    self.driver.find_element(By.ID, "id_civil_state").send_keys("2")
    self.driver.find_element(By.ID, "id_sexuality").send_keys("2")
    self.driver.find_element(By.ID, "id_works").send_keys("2")
    self.driver.find_element(By.CSS_SELECTOR, "button").click()
    self.driver.find_element(By.LINK_TEXT, "Come back to Census Menu").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(6) .card-title").click()
    self.driver.find_element(By.LINK_TEXT, "Exportar en Excel").click()

  #Hay que estra logueado para realizar una exportaci??n
  #Probamos a exportar sin login
  def test_exportwronglogin(self):
    self.driver.get("http://127.0.0.1:8000/census/")
    self.driver.set_window_size(603, 684)
    self.driver.find_element(By.CSS_SELECTOR, ".container2").click()
    self.driver.find_element(By.CSS_SELECTOR, "h1").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col:nth-child(6) .card-title").click()
    self.driver.find_element(By.CSS_SELECTOR, "html").click()
    self.driver.find_element(By.LINK_TEXT, "Exportar en Excel").click()