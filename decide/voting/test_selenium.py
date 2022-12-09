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