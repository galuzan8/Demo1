import sys
# sys.path.append("C:\Users\uzang\PycharmProjects\Demo1\\")
# sys.path.append('/home/galu/demo1/')
import constants as C
import pages
import time

def test_homepage(driver):
    homepage = pages.Homepage(driver)
    assert homepage.getCurrentUrl() == C.HOMEPAGE_URL

def test_homepage_login(driver):
    homepage = pages.Homepage(driver)
    loginBubble = homepage.getLoginBubble()
    time.sleep(8)
    loginBubble.setEmail(C.LOGINEMAIL)
    loginBubble.setPassword(C.LOGINPASSWORD)
    homepage = loginBubble.submitLogin()
    time.sleep(8)
    homepage.navigateToHomePage()
    assert homepage.VerifyLogin() is True

def test_WebDevelopmentPageByClick(driver):
    homepage = pages.Homepage(driver)
    CategoriesBubble = homepage.getCategoriesViaHover()
    time.sleep(1)
    CategoriesBubble.openWebDevelopment()
    time.sleep(10)
    assert CategoriesBubble.getCurrentUrl() == C.WEBDEVLOPMENT_URL

def test_SearchSeleniumFromWebDevelopmentPage(driver):
    WebDevelopmentPage = pages.WebDevelopmentPage(driver)
    ResultsPage = WebDevelopmentPage.UseSearchBox('selenium')
    time.sleep(5)
    if ResultsPage.FilterResultsByPrice('free'):
        time.sleep(10)
        freeCourses = ResultsPage.countFreeCourses()
        allCourses = ResultsPage.countAllCourses()
        assert ['Selenium' in title for title in ResultsPage.getCoursesTitles()]
        assert freeCourses >= 2 and freeCourses < 10
        # assert allCourses == freeCourses

