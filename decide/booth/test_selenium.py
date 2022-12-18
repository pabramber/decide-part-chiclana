from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

from base.tests import BaseTestCase

from django.conf import settings

from django.contrib.auth.models import User
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from census.models import Census

class VotingSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()
        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        u = User(username='us')
        u.set_password("egc.decide")
        u.save()

        censo = Census.objects.create(voting_id=v.id, voter_id=u.id, name='a', surname='a',city= 'a', a_community='a', gender='a', 
                    born_year=2001, civil_state='a', sexuality='a',works= 1)
        censo.save()

        super().setUp()  

        

    def tearDown(self):
        admin = User.objects.get(username='admin')
        admin.is_superuser = False
        admin.save()
        self.driver.quit()
        self.base.tearDown()

    def test_no_votings(self):
        self.driver.get(f'{self.live_server_url}/authentication/register/')
        self.driver.set_window_size(1440, 752)
        self.driver.find_element(By.ID, "id_username").send_keys("albertobm")
        self.driver.find_element(By.ID, "id_password1").send_keys("egc.decide")
        self.driver.find_element(By.ID, "id_password2").click()
        self.driver.find_element(By.ID, "id_password2").send_keys("egc.decide")
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_password1").click()
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys("a@gmail.com")
        self.driver.find_element(By.ID, "id_first_name").click()
        self.driver.find_element(By.ID, "id_first_name").send_keys("a")
        self.driver.find_element(By.ID, "id_last_name").click()
        self.driver.find_element(By.ID, "id_last_name").send_keys("a")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.get(f'{self.live_server_url}/authentication/login-view/')
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("albertobm")
        self.driver.find_element(By.ID, "id_password1").click()
        self.driver.find_element(By.ID, "id_password1").send_keys("egc.decide")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.get(f'{self.live_server_url}/booth/')
        # Check no votings avaible
        self.assertTrue((self.driver.find_element(By.ID, "no-voting")))

    def test_list_votings(self):
        self.driver.get(f"{self.live_server_url}/admin/")
        self.driver.set_window_size(1440, 752)
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("qwerty")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-row").click()

        self.driver.find_element(By.LINK_TEXT, "Votings").click()
        self.driver.find_element(By.NAME, '_selected_action').click()
        self.driver.find_element(By.XPATH, "//select[@name='action']").click()
        self.driver.find_element(By.XPATH, "//select[@name='action']//child::option[@value='start']").click()
        self.driver.find_element(By.XPATH, "//button[@name='index']").click()

        self.driver.get(f'{self.live_server_url}/authentication/login-view/')
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("us")
        self.driver.find_element(By.ID, "id_password1").click()
        self.driver.find_element(By.ID, "id_password1").send_keys("egc.decide")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.get(f'{self.live_server_url}/booth/')
        # Check no votings avaible
        self.assertTrue((self.driver.find_element(By.ID, "table-element")))