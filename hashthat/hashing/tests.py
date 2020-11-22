from django.test import TestCase
from django.core.exceptions import ValidationError
from selenium import webdriver
from .forms import HashForm
from .models import Hash
from time import sleep
import hashlib

# Create your tests here.

class FunctionalTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_is_there_homepage(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Enter hash here: ', self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.browser.find_element_by_name('submit').click()
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        sleep(5)
        self.assertIn('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', self.browser.page_source)
        
    def tearDown(self):
        self.browser.quit()


class UnitTestCase(TestCase):

    def test_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/homepage.html')

    def test_hash_form(self):
        form = HashForm(data = {'text':'hello'})
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', text_hash)

    def saveHash(self):
        haash = Hash()
        haash.text = 'hello'
        haash.haash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        haash.save()
        return haash

    def test_hash_object(self):
        haash = self.saveHash()
        pulled_hash = Hash.objects.get(haash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
        self.assertEqual(pulled_hash.haash, haash.haash)

    def test_viewing_hash(self):
        haash = self.saveHash()
        response = self.client.get('/hash/2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824/')
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        def badHash():
            haash = Hash()
            haash.haash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824garbage'
            haash.full_clean()
        self.assertRaises(ValidationError, badHash)

        





