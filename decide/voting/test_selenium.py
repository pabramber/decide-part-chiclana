from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase

from django.contrib.auth.models import User

class VotingSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.browser = webdriver.Chrome(options=options)


    def tearDown(self):
        admin = User.objects.get(username='admin')
        admin.is_superuser = False
        admin.save()
        self.browser.quit()


    def test_create_ranked_question(self):
        self.browser.get(self.live_server_url + '/admin/')
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('qwerty')
        password_input.send_keys(Keys.ENTER)

        self.browser.get(self.live_server_url + '/admin/voting/question/add/')
        desc_input = self.browser.find_element_by_name("desc")
        desc_input.send_keys('Test question')
        desc_input.send_keys(Keys.ENTER)

        tipo_input = self.browser.find_element_by_name("tipo")
        tipo_input.send_keys('R')
        tipo_input.send_keys(Keys.ENTER)

        opt1_input = self.browser.find_element_by_name("options-0-option")
        opt1_input.send_keys('Option 1')
        opt1_input.send_keys(Keys.ENTER)

        opt2_input = self.browser.find_element_by_name("options-1-option")
        opt2_input.send_keys('Option 2')
        opt2_input.send_keys(Keys.ENTER)

        opt3_input = self.browser.find_element_by_name("options-2-option")
        opt3_input.send_keys('Option 3')
        opt3_input.send_keys(Keys.ENTER)

        save = self.browser.find_element_by_name("_continue")
        save.click()

        create_ordination = self.browser.find_element_by_name("create_ordination")
        create_ordination.click()

        save2 = self.browser.find_element_by_name("_continue")
        save2.click()

        self.assertEquals('Test question', self.browser.find_element_by_name("desc").get_attribute('value'))
        self.assertEquals('R', self.browser.find_element_by_name("tipo").get_attribute('value'))

        self.assertIn('Option 1, Option 2, Option 3', self.browser.find_element_by_name("options-0-option").get_attribute('value'))
        self.assertIn('Option 1, Option 3, Option 2', self.browser.find_element_by_name("options-1-option").get_attribute('value'))
        self.assertIn('Option 2, Option 1, Option 3', self.browser.find_element_by_name("options-2-option").get_attribute('value'))
        self.assertIn('Option 2, Option 3, Option 1', self.browser.find_element_by_name("options-3-option").get_attribute('value'))
        self.assertIn('Option 3, Option 1, Option 2', self.browser.find_element_by_name("options-4-option").get_attribute('value'))
        self.assertIn('Option 3, Option 2, Option 1', self.browser.find_element_by_name("options-5-option").get_attribute('value'))

'''
El test de TestSaveVotingFile funciona correctamente en local, cuando el usuario ya existe en la base de datos,
creado con el comando: psql -c "create user <usuario> with password '<contraseña>'".
Cuando se crea al usuario dentro del propio test, muestra un error 500 al realizar el tally.
Dejo el test comentado, de manera que se pueda probar en local.

class TestSaveVotingFile(StaticLiveServerTestCase):

    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()
    
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
        admin = User.objects.get(username='admin')
        admin.is_superuser = False
        admin.save()

        self.base.tearDown() 
    
    def test_save_voting_file(self):
        driver = self.driver

        # Log in
        # Comentar una de las dos siguientes lineas, según cómo se quiera probar
        driver.get("http://localhost:8000/admin/login/?next=/admin/")
        # driver.get(f'{self.live_server_url}/admin/')
        driver.find_element(By.ID, 'id_username').click()
        driver.find_element(By.ID, 'id_username').send_keys('dantorval')
        driver.find_element(By.ID, 'id_password').click()
        driver.find_element(By.ID, 'id_password').send_keys('dantorval')
        driver.find_element(By.XPATH, "//input[@value='Log in']").click()
                
        # Create question
        driver.find_element(By.LINK_TEXT, 'Questions').click()
        driver.find_element(By.LINK_TEXT, 'ADD QUESTION').click()
        driver.find_element(By.ID, 'id_desc').click()
        driver.find_element(By.ID, 'id_desc').send_keys('question_desc')
        driver.find_element(By.ID, 'id_options-0-option').click()
        driver.find_element(By.ID, 'id_options-0-option').send_keys('option_1')
        driver.find_element(By.ID, 'id_options-1-option').click()
        driver.find_element(By.ID, 'id_options-1-option').send_keys('option_2')
        driver.find_element(By.XPATH, "//input[@value='Save']").click()

        # Create auth
        driver.find_element(By.LINK_TEXT, 'Home').click()
        driver.find_element(By.LINK_TEXT, 'Auths').click()
        driver.find_element(By.LINK_TEXT, 'ADD AUTH').click()
        driver.find_element(By.ID, 'id_name').click()
        driver.find_element(By.ID, 'id_name').send_keys('auth_name')
        driver.find_element(By.ID, 'id_url').click()
        driver.find_element(By.ID, 'id_url').send_keys(f'{self.live_server_url}')
        driver.find_element(By.ID, 'id_me').click()
        driver.find_element(By.XPATH, "//input[@value='Save']").click()

        # Create voting
        driver.find_element(By.LINK_TEXT, 'Home').click()
        driver.find_element(By.LINK_TEXT, 'Votings').click()
        driver.find_element(By.LINK_TEXT, 'ADD VOTING').click()
        driver.find_element(By.ID, 'id_name').click()
        driver.find_element(By.ID, 'id_name').send_keys('voting_name')
        driver.find_element(By.ID, 'id_desc').click()
        driver.find_element(By.ID, 'id_desc').send_keys('voting_desc')
        driver.find_element(By.XPATH, "//select[@id='id_question']").click()
        driver.find_element(By.XPATH, "//select[@id='id_question']//child::option[last()]").click()
        driver.find_element(By.XPATH, "//select[@id='id_auths']//child::option[last()]").click()
        driver.find_element(By.XPATH, "//input[@value='Save']").click()
        
        # Start, Stop, Tally & Save voting
        driver.find_element(By.NAME, '_selected_action').click()
        driver.find_element(By.XPATH, "//select[@name='action']").click()
        driver.find_element(By.XPATH, "//select[@name='action']//child::option[@value='start']").click()
        driver.find_element(By.XPATH, "//button[@name='index']").click()
        driver.find_element(By.NAME, '_selected_action').click()
        driver.find_element(By.XPATH, "//select[@name='action']").click()
        driver.find_element(By.XPATH, "//select[@name='action']//child::option[@value='stop']").click()
        driver.find_element(By.XPATH, "//button[@name='index']").click()
        driver.find_element(By.NAME, '_selected_action').click()
        driver.find_element(By.XPATH, "//select[@name='action']").click()
        driver.find_element(By.XPATH, "//select[@name='action']//child::option[@value='tally']").click()        
        driver.find_element(By.XPATH, "//button[@name='index']").click()
            
        # Check no file
        driver.find_element(By.XPATH, "//tr[@class='row1']//child::th[@class='field-name']").click()
        text_file = driver.find_element(By.CSS_SELECTOR, ".field-file .readonly").text
        self.assertEqual("", text_file)
        driver.execute_script("window.history.go(-1)")
        
        # Save voting
        driver.find_element(By.NAME, '_selected_action').click()
        driver.find_element(By.XPATH, "//select[@name='action']").click()
        driver.find_element(By.XPATH, "//select[@name='action']//child::option[@value='save']").click()
        driver.find_element(By.XPATH, "//button[@name='index']").click()

        # Check file
        driver.find_element(By.XPATH, "//tr[@class='row1']//child::th[@class='field-name']").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, 'voting/files/').click()
        driver.execute_script("window.history.go(-1)")
        
        # En caso de probar con la dirección "f'{self.live_server_url}/admin/'",
        # comentar las lineas de Delete auth y Delete question.
        # Delete auth
        driver.find_element(By.LINK_TEXT, 'Home').click()
        driver.find_element(By.LINK_TEXT, 'Auths').click()
        driver.find_element(By.NAME, '_selected_action').click()
        driver.find_element(By.NAME, 'action').click()
        driver.find_element(By.XPATH, "//option[@value='delete_selected']").click()
        driver.find_element(By.XPATH, "//button[@name='index']").click()
        driver.find_element(By.XPATH, '//input[@value="Yes, I\'m sure"]').click()
        driver.find_element(By.NAME, '_selected_action').click()
        driver.find_element(By.NAME, 'action').click()
        driver.find_element(By.XPATH, "//option[@value='delete_selected']").click()
        driver.find_element(By.XPATH, "//button[@name='index']").click()
        driver.find_element(By.XPATH, '//input[@value="Yes, I\'m sure"]').click()

        # Delete question
        driver.find_element(By.LINK_TEXT, 'Home').click()
        driver.find_element(By.LINK_TEXT, 'Questions').click()
        driver.find_element(By.NAME, '_selected_action').click()
        driver.find_element(By.NAME, 'action').click()
        driver.find_element(By.XPATH, "//option[@value='delete_selected']").click()
        driver.find_element(By.XPATH, "//button[@name='index']").click()
        driver.find_element(By.XPATH, '//input[@value="Yes, I\'m sure"]').click()
'''