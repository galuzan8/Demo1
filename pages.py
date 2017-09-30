from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants as C

class BasePage(object):
    """ This is the basic page class, all other pages inherit from this class"""

    def __init__(self, driver):
        self.driver = driver
        if C.BLANKPAGE_STR in driver.current_url:
            self.navigateToHomePage()

    def fill_form_by_id(self, form_element_id, value):
        """ This function fills a form by an id"""
        return self.driver.find_element_by_id(form_element_id).send_keys(value)

    def UseSearchBox(self, str):
        """ Search for something in the search box"""
        # Fill the form
        self.driver.find_element_by_id(C.ID_SEARCBOX)
        self.fill_form_by_id(C.ID_SEARCBOX, str)

        # Click the search button
        self.driver.find_element_by_class_name(C.CLASS_SEARCHBOX_BUTTON).click()
        return ResultsPage(self.driver)

    def getCurrentUrl(self):
        """ Returns current page url """
        return self.driver.current_url

    def navigateToHomePage(self):
        """ Returns the browser to the homepage """
        self.driver.get(C.HOMEPAGE_URL)

    def waitForPage(self, element_locator, value):
        # Waits for a page to load. possible element locator: ID, XPATH, CLASS
        if 'ID' in element_locator.upper():
            by = By.ID
        elif 'CLASS' in element_locator.upper():
            by = By.CLASS_NAME
        elif 'XPATH' in element_locator.upper():
            by = By.XPATH
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
        finally:
            return True

class Homepage(BasePage):
    """ Homepage class"""

    def getLoginBubble(self):
        """ Finds login bubble and clicks it """
        self.waitForPage('XPATH', C.XPATH_LOGIN_BUBBLE)
        self.driver.find_element_by_xpath(C.XPATH_LOGIN_BUBBLE).click()
        return LoginBubble(self.driver)

    def getCategoriesViaHover(self):
        """ Use the categories button to get Web Development courses"""
        categories = self.driver.find_element_by_class_name(C.CLASS_CATEGORIES)
        # Hover mouse
        ActionChains(self.driver).move_to_element(categories).perform()
        return CategoriesBubble(self.driver)

    def VerifyLogin(self):
        """ Verifies user avatar appears """
        if self.driver.find_element_by_class_name(C.CLASS_LOGGEDIN):
            return True
        return False

class LoginBubble(BasePage):

    def setEmail(self, email):
        """ Sets the email in LoginBubble """
        self.fill_form_by_id(C.ID_LOGINEMAIL, email)

    def setPassword(self, password):
        """ Sets the password in LoginBubble """
        self.fill_form_by_id(C.ID_LOGINPASSWORD, password)

    def submitLogin(self):
        """ Click the login button in LoginBubble """
        self.driver.find_element_by_id(C.ID_SUBMITLOGIN).click()
        return Homepage(self.driver)

class CategoriesBubble(BasePage):

    def openWebDevelopment(self):
        """ Opens Web Development Page via click"""
        p = self.driver.find_element_by_xpath(C.XPATH_DEVELOPMENT)
        hover = ActionChains(self.driver).move_to_element(p).perform()
        p = self.driver.find_element_by_xpath(C.XPATH_WEBDEVELOPMENT).click()
        return WebDevelopmentPage(self.driver)

class WebDevelopmentPage(BasePage):
    def foo(self):
        return

class ResultsPage(BasePage):

    def FilterResultsByPrice(self, price):
        """ Filter results by 'Paid' or 'Free'"""
        self.driver.find_element_by_id('label-top-filter-price').click()
        if 'free' in price.lower():
            self.driver.find_element_by_xpath(C.XPATH_FREEFILTER).click()
            return True
        elif 'paid' in price.lower():
            self.driver.find_element_by_xpath(C.XPATH_PAIDFILTER).click()
            return True
        else:
            print "Must specify Paid or Free"
            return False

    def countFreeCourses(self):
        """ Count how many free courses """
        return len(self.driver.find_elements_by_class_name(C.CLASS_RESULT_FREE_COURSES))

    def countAllCourses(self):
        """ Count all of the courses """
        return len(self.driver.find_elements_by_class_name(C.CLASS_RESULT_COURSES))

    def getCoursesTitles(self):
        """ returns a list of all the courses titles """
        allRes = self.driver.find_elements_by_class_name(C.CLASS_RESULT_COURSES)
        allResTitles = [p.text.split('\n')[0] for p in allRes]
        return allResTitles
