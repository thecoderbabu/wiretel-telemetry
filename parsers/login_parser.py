from selenium.webdriver.common.by import By
from locators.login_locator import LoginLocators

class TableRow:
    def __init__(self, row):
        self.row = row

    @property
    def table_data(self):
        locator = LoginLocators.TABLE_DATA
        return [e.text for e in self.row.find_elements(By.CSS_SELECTOR, locator)]

class LoginParser:
    """
    Given one of the specific qutoe divs
    """

    def __init__(self, parent):
        self.parent = parent

    @property
    def data(self):
        locator = LoginLocators.TABLE_ROW
        return [TableRow(e) for e in self.parent.find_elements(By.CSS_SELECTOR, locator)]


