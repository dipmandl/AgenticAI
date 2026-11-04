"""
Page Object Model — Release Notes Dashboard

Encapsulates all Selenium interactions with the Release Notes Dashboard UI.
Used by step definitions in steps/step_json_export.py and steps/step_regression.py.

Story: COD-9 — Export Release Notes to JSON File
App:   file:///C:/Users/DipakMandlik/Desktop/AgenticAI/Final_implementation/AgenticAI/
       product_release_dashboard/index.html
"""

import time
from typing import List, Optional

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ReleaseDashboardPage:
    """Page Object for the Release Notes Dashboard SPA."""

    # ------------------------------------------------------------------
    # Selectors
    # ------------------------------------------------------------------

    # Export / Import buttons
    EXPORT_JSON_BTN   = (By.ID, "export-json-button")
    EXPORT_CSV_BTN    = (By.ID, "export-csv-button")
    IMPORT_JSON_BTN   = (By.ID, "import-json-button")

    # Form fields
    FORM              = (By.ID, "release-form")
    PRODUCT_INPUT     = (By.ID, "product")
    VERSION_INPUT     = (By.ID, "version")
    TEAM_NAME_INPUT   = (By.ID, "teamName")
    TITLE_INPUT       = (By.ID, "title")
    DESCRIPTION_INPUT = (By.ID, "description")
    RELEASE_DATE_INPUT = (By.ID, "releaseDate")
    BREAKING_CHECKBOX = (By.ID, "breaking")
    SUBMIT_BTN        = (By.ID, "submit-button")
    CANCEL_EDIT_BTN   = (By.ID, "cancel-edit-button")

    # Release list
    RELEASE_LIST      = (By.ID, "release-list")
    RELEASE_CARDS     = (By.CSS_SELECTOR, "#release-list .release-card")
    EDIT_BTNS         = (By.CSS_SELECTOR, ".edit-btn")
    DELETE_BTNS       = (By.CSS_SELECTOR, ".delete-btn")

    # Misc
    TRANSFER_STATUS   = (By.ID, "transfer-status")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait   = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, url: str) -> None:
        self.driver.get(url)
        self._wait_for_page_ready()

    def reload(self) -> None:
        self.driver.refresh()
        self._wait_for_page_ready()

    def _wait_for_page_ready(self) -> None:
        """Wait until the release-list element is present in the DOM."""
        self.wait.until(EC.presence_of_element_located(self.RELEASE_LIST))

    # ------------------------------------------------------------------
    # Export JSON button
    # ------------------------------------------------------------------

    def is_export_json_button_visible(self) -> bool:
        """Return True if the Export JSON button is present and displayed."""
        try:
            btn = self.wait.until(EC.visibility_of_element_located(self.EXPORT_JSON_BTN))
            return btn.is_displayed()
        except TimeoutException:
            return False

    def count_export_json_buttons(self) -> int:
        """Return the number of Export JSON buttons in the DOM (TC-014)."""
        try:
            elements = self.driver.find_elements(*self.EXPORT_JSON_BTN)
            return len(elements)
        except NoSuchElementException:
            return 0

    def click_export_json(self) -> None:
        """Click the Export JSON button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.EXPORT_JSON_BTN))
        btn.click()

    # ------------------------------------------------------------------
    # Form interactions
    # ------------------------------------------------------------------

    def fill_form(
        self,
        product: str,
        version: str,
        team_name: str,
        title: str,
        description: str,
        release_date: str,
        is_breaking: bool = False,
    ) -> None:
        """Fill all release-note form fields."""
        self.driver.find_element(*self.PRODUCT_INPUT).clear()
        self.driver.find_element(*self.PRODUCT_INPUT).send_keys(product)

        self.driver.find_element(*self.VERSION_INPUT).clear()
        self.driver.find_element(*self.VERSION_INPUT).send_keys(version)

        self.driver.find_element(*self.TEAM_NAME_INPUT).clear()
        self.driver.find_element(*self.TEAM_NAME_INPUT).send_keys(team_name)

        self.driver.find_element(*self.TITLE_INPUT).clear()
        self.driver.find_element(*self.TITLE_INPUT).send_keys(title)

        self.driver.find_element(*self.DESCRIPTION_INPUT).clear()
        self.driver.find_element(*self.DESCRIPTION_INPUT).send_keys(description)

        self.driver.find_element(*self.RELEASE_DATE_INPUT).send_keys(release_date)

        checkbox = self.driver.find_element(*self.BREAKING_CHECKBOX)
        if checkbox.is_selected() != is_breaking:
            checkbox.click()

    def submit_form(self) -> None:
        """Click the Add / Update Release Note submit button."""
        self.driver.find_element(*self.SUBMIT_BTN).click()

    def click_cancel_edit(self) -> None:
        self.driver.find_element(*self.CANCEL_EDIT_BTN).click()

    # ------------------------------------------------------------------
    # Release list
    # ------------------------------------------------------------------

    def get_release_cards(self) -> List[WebElement]:
        """Return all currently visible release card elements."""
        try:
            return self.driver.find_elements(*self.RELEASE_CARDS)
        except NoSuchElementException:
            return []

    def count_release_cards(self) -> int:
        return len(self.get_release_cards())

    def get_card_title(self, card: WebElement) -> str:
        return card.find_element(By.CSS_SELECTOR, ".release-title").text

    def click_edit_first_card(self) -> None:
        """Click the Edit button on the first release card."""
        cards = self.get_release_cards()
        if not cards:
            raise AssertionError("No release cards found to edit.")
        cards[0].find_element(By.CSS_SELECTOR, ".edit-btn").click()

    def click_delete_first_card(self) -> None:
        """Click the Delete button on the first release card (handles confirm dialog)."""
        cards = self.get_release_cards()
        if not cards:
            raise AssertionError("No release cards found to delete.")
        cards[0].find_element(By.CSS_SELECTOR, ".delete-btn").click()
        # Accept the browser confirm dialog
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception:
            pass

    def is_card_with_title_visible(self, title: str) -> bool:
        """Return True if at least one release card shows the given title."""
        cards = self.get_release_cards()
        for card in cards:
            if title in self.get_card_title(card):
                return True
        return False

    # ------------------------------------------------------------------
    # Edit an existing release
    # ------------------------------------------------------------------

    def edit_first_release_title(self, new_title: str) -> None:
        """Open edit mode for the first card, change title, and save."""
        self.click_edit_first_card()
        title_input = self.wait.until(EC.visibility_of_element_located(self.TITLE_INPUT))
        title_input.clear()
        title_input.send_keys(new_title)
        self.submit_form()

    # ------------------------------------------------------------------
    # Misc UI helpers
    # ------------------------------------------------------------------

    def get_transfer_status_text(self) -> str:
        try:
            return self.driver.find_element(*self.TRANSFER_STATUS).text
        except NoSuchElementException:
            return ""

    def navigate_all_views(self) -> None:
        """
        For a single-page application with no routing, this scrolls through
        the page sections to verify they render without JS errors.
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)
        self.driver.execute_script("window.scrollTo(0, 0);")
