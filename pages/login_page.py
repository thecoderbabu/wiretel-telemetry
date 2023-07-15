from typing import List
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

from locators.login_locator import LoginLocators
from locators.usage_page_locator import DataUsage
from parsers.login_parser import LoginParser


class LoginPage:
    def __init__(self, browser):
        self.browser = browser

    @property
    def table_head(self):
        return [
            e.text
            for e in self.browser.find_elements(
                By.CSS_SELECTOR, LoginLocators.TABLE_HEAD
            )
        ]

    @property
    def table_content(self) -> List[LoginParser]:
        return [
            LoginParser(e)
            for e in self.browser.find_elements(
                By.CSS_SELECTOR, DataUsage.TABLE_LOCATOR
            )
        ]

    @property
    def username_select(self):
        element = self.browser.find_element(
            By.CSS_SELECTOR, LoginLocators.USERNAME_LOCATOR
        )
        return element

    @property
    def password_select(self):
        element = self.browser.find_element(
            By.CSS_SELECTOR, LoginLocators.PASSWORD_LOCATOR
        )
        return element

    @property
    def signin_button(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, LoginLocators.SIGNIN_LOCATOR
        )

    @property
    def myusage_link(self):
        self.browser.switch_to.default_content()
        return self.browser.find_element(
            By.XPATH, LoginLocators.MYUSAGE_LOCATOR
        )

    def username_input(self, username: str):
        self.username_select.send_keys(username)

    def next_select(self):
        self.browser.switch_to.default_content()
        return [x for x in self.browser.find_elements(
            By.CSS_SELECTOR, LoginLocators.NEXT_LOCATOR
        )]

    def password_input(self, password: str):
        self.password_select.send_keys(password)

    def input_form(self, username: str, password: str):
        self.username_input(username)
        try:
            self.password_input(password)
        except NoSuchElementException:
            raise InvalidTagForAuthorError(
                f"Author '{username}' does not have any quotes tagged with '{password}'."
            )
        self.browser.switch_to.active_element
        # self.signin_button.click()
        self.signin_button.send_keys("\n")
        time.sleep(3)
        # self.myusage_link.click()
        self.myusage_link.send_keys("\n")
        time.sleep(10)
        self.browser.switch_to.default_content()
        tabledata = []
        contents = self.table_content
        flag = True
        for row in contents:
            # print("here again row: ",row)
            for data in row.data:
                tabledata.append(data.table_data)
        while flag:
            flag1 = True
            chomu = self.next_select()
            for x in chomu:
                # print("Here",x.get_property('href'),type(x),x.text)
                if x.text == "Next":
                    flag1 = False
                    if x.is_enabled():
                        # x.click()
                        x.send_keys("\n")
                        time.sleep(5)
                        self.browser.switch_to.default_content()
                        contents = self.table_content
                        for row in contents:
                            # print("here again row: ",row)
                            for data in row.data:
                                tabledata.append(data.table_data)
                        break
                    else:
                        flag = False
            if flag1:
                break

        return self.table_head, tabledata


class InvalidTagForAuthorError(ValueError):
    pass
