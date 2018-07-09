#-------------------------FUNCTIONAL TESTS-------------------------------------
# This File tests high-level functionality using Selenium Browser Automation

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HelperFunctions():
    def helper_search_tag_contains_text(self,tagname,text_to_find):
        data = self.browser.find_element_by_tag_name(tagname)
        self.assertIn(text_to_find, data.text)

    def helper_check_current_url_matches_expected(self,relative_expected_url):
        self.assertEqual(self.browser.current_url,
                         self.BASE_URL + relative_expected_url,msg="URL was "+self.browser.current_url)

    def helper_find_and_click_on_link(self,data,is_name=False):
        if is_name==True:
            link = self.browser.find_element_by_name(data)
        else:
            link = self.browser.find_element_by_link_text(data)
        link.click()

    def helper_find_form_element_by_id_and_fill(self,form_field_id,data,enter=False):
        field = self.browser.find_element_by_id(form_field_id)
        field.send_keys(data)
        if enter:
            field.send_keys(Keys.ENTER)


class NewUserTest(LiveServerTestCase,HelperFunctions):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='chromedriver.exe')
        self.BASE_URL = self.live_server_url

    def tearDown(self):
        self.browser.quit()

    def test_new_user_registers(self):
        # DJ has heard about a cool new app to earn crypto moolah
        # He goes to to website to check it out
        self.browser.get(self.BASE_URL)

        # He sees the home page saying 'Welcome to Equity Network's EQit App'
        self.helper_search_tag_contains_text('body',"Welcome to Equity Network's EQit App")
        # He sees the title 'Equity Network' on the tab
        self.assertIn('Equity Network',self.browser.title,
                      msg='Title was'+self.browser.title)
        # He sees two icons on the right, login and signup
        # he clicks on login
        self.helper_find_and_click_on_link('Login')
        # he is taken to the login page
        self.helper_check_current_url_matches_expected('/account/login/')
        # He sees two links, one for user and one for provider
        # He doesn't know what to do so clicks on user login
        self.helper_find_and_click_on_link('user-login',True)
        # he is redirected to a page with a login form
        self.helper_check_current_url_matches_expected('/account/login/user/')
        
        # he sees two fields, email and password
        self.helper_find_form_element_by_id_and_fill('id_email','dj123@email.com')
        self.helper_find_form_element_by_id_and_fill('id_password','password123',True)
        # he is a klutz, so he forgot that he hasn't created an account yet.
        # Sure enough nothing happens and he is greeted by an error message that the credentials are wrong
        self.helper_search_tag_contains_text('body','Username or Password Does not Match')
        
        # Now he sees that there is another link for signing up and clicks on it
        self.helper_find_and_click_on_link('user-signup',True)
        # he is redirected to a user signup page
        self.helper_check_current_url_matches_expected('/account/sign-up/user/')
        
        # he sees three form fields: email, password and password confirmation
        self.helper_find_form_element_by_id_and_fill('id_email','dj123@email.com')
        self.helper_find_form_element_by_id_and_fill('id_password1','password123')
        # remember, he is a clutz. He puts a different password in the password confirmation
        self.helper_find_form_element_by_id_and_fill('id_password2','password1',True)
       
       # Of course, the signup fails with an error -> The two password fields didn't match.
        # He is still at the same page
        self.helper_check_current_url_matches_expected('/account/sign-up/user/')
        self.helper_search_tag_contains_text('body',"The two password fields didn't match.")
        
        # now he enters the correct username and password
        self.helper_find_form_element_by_id_and_fill('id_email','dj123@email.com')
        self.helper_find_form_element_by_id_and_fill('id_password1','password123')
        self.helper_find_form_element_by_id_and_fill('id_password2','password123',True)

        # He is redirected to the user login page
        self.assertEqual(self.browser.current_url,
                         self.BASE_URL + '/account/login/user/',msg="URL was "+self.browser.current_url)
        # A message in green says that his account has been created and he can log in
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn("Your account has been created. Please proceed to log in.", body.text)
        
        # So he logs in
        self.helper_find_form_element_by_id_and_fill('id_email','dj123@email.com')
        self.helper_find_form_element_by_id_and_fill('id_password','password123',True)

        # He is greeted by a page that looks like his profile and a message -> You are now logged in.
        self.helper_check_current_url_matches_expected('/account/profile/')
        self.helper_search_tag_contains_text('body','You are now logged in.')

        # He suddenly remembers he has urgent work, so he searches for log out in the right dropdown and clicks it
        self.helper_find_and_click_on_link('right-dropdown',True)
        self.helper_find_and_click_on_link('logout',True)
        
        # He is returned to the login page with the message -> 'You have been logged out.'
        self.helper_check_current_url_matches_expected('/account/login/')
        self.helper_search_tag_contains_text('body','You have been logged out.')

        # He closes his browser ## This gets rid of saved sessions
        self.browser.quit()

        # Later he comes back to set up his profile
        self.browser = webdriver.Chrome(executable_path='chromedriver.exe')
        self.browser.get(self.live_server_url)
        
        # Clicks on the login button
        self.helper_find_and_click_on_link('Login')
        ## No need to check link again
        # Being a klutz as usual, he clicks on the provider login and enters his credentials
        
        self.helper_find_and_click_on_link('provider-login',True)
        self.helper_check_current_url_matches_expected('/account/login/provider/')
        self.helper_find_form_element_by_id_and_fill('id_email','dj123@email.com')
        self.helper_find_form_element_by_id_and_fill('id_password','password123',True)

        # Oh, it seems that he used the wrong login page...duh
        # Nevermind, he is redirected to the correct one
        #try:
        #    element = WebDriverWait(self.browser, 10).until(
        #EC.presence_of_element_located((By.ID, "id_email")))
        #except:
        #    self.fail()
        self.helper_check_current_url_matches_expected('/account/login/user/')
        self.helper_search_tag_contains_text('body','You were using the wrong login page. Login Here')
        self.helper_find_form_element_by_id_and_fill('id_email','dj123@email.com')
        self.helper_find_form_element_by_id_and_fill('id_password','password123',True)

        # Now he is on his profiles page
        # He notices that the details are empty so he clicks on edit profile
        self.helper_find_and_click_on_link('Edit')

        # He is redirected to the edit page
        self.helper_check_current_url_matches_expected('/account/profile/edit/')
        

class NewProviderTest(LiveServerTestCase,HelperFunctions):
    
    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='chromedriver.exe')
        self.BASE_URL = self.live_server_url

    def tearDown(self):
        self.browser.quit()