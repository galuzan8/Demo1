import pytest
from selenium import webdriver
import constants as C

@pytest.fixture(scope='module')
def driver(request):
    driverObj = webdriver.Chrome(executable_path=C.DRIVER_PATH)
    def tearDown():
        driverObj.close()
    request.addfinalizer(tearDown)
    return driverObj

