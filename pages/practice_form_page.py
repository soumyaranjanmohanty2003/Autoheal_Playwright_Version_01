"""Page Object for the DemoQA Practice Form (https://demoqa.com/automation-practice-form)."""
import re

from playwright.sync_api import Page


class PracticeFormPage:
    URL = "/automation-practice-form"

    def __init__(self, page: Page):
        self.page = page

    # ---- navigation -------------------------------------------------
    def open(self):
        self.page.goto(self.URL)
        self._dismiss_ads()

    def _dismiss_ads(self):
        # DemoQA renders ad banners that can overlap form fields/buttons.
        close_ad = self.page.locator("#close-fixedban")
        if close_ad.is_visible():
            close_ad.click()

    # ---- form fields --------------------------------------------------
    def fill_name(self, first_name: str, last_name: str):
        self.page.locator("#firstName").fill(first_name)
        self.page.locator("#lastName").fill(last_name)

    def fill_email(self, email: str):
        self.page.locator("#userEmail").fill(email)

    def select_gender(self, gender: str):
        gender_index = {"Male": 1, "Female": 2, "Other": 3}[gender]
        self.page.locator(f"label[for='gender-radio-{gender_index}']").click()

    def fill_mobile(self, mobile: str):
        self.page.locator("#userNumber").fill(mobile)

    def set_date_of_birth(self, day: str, month: str, year: str):
        self.page.locator("#dateOfBirthInput").click()
        self.page.locator(".react-datepicker__month-select").select_option(label=month)
        self.page.locator(".react-datepicker__year-select").select_option(year)
        day_option = self.page.locator(
            ".react-datepicker__day:not(.react-datepicker__day--outside-month)",
            has_text=re.compile(rf"^{day}$"),
        )
        day_option.first.click()

    def add_subject(self, subject: str):
        subject_input = self.page.locator("#subjectsInput")
        subject_input.fill(subject)
        subject_input.press("Enter")

    def select_hobbies(self, hobbies: list[str]):
        hobby_index = {"Sports": 1, "Reading": 2, "Music": 3}
        for hobby in hobbies:
            self.page.locator(f"label[for='hobbies-checkbox-{hobby_index[hobby]}']").click()

    def fill_current_address(self, address: str):
        self.page.locator("#currentAddress").fill(address)

    def select_state_and_city(self, state: str, city: str):
        self._select_react_dropdown("#state", state)
        self._select_react_dropdown("#city", city)

    def _select_react_dropdown(self, container_selector: str, value: str):
        self.page.locator(container_selector).click()
        self.page.keyboard.type(value)
        self.page.keyboard.press("Enter")

    def submit(self):
        self._dismiss_ads()
        submit_button = self.page.locator("#submit")
        submit_button.scroll_into_view_if_needed()
        submit_button.click()

    # ---- confirmation modal -------------------------------------------
    def get_modal_title(self) -> str:
        return self.page.locator("#example-modal-sizes-title-lg").inner_text()

    def get_modal_data(self) -> dict:
        rows = self.page.locator(".table-responsive tbody tr")
        data = {}
        for row in rows.all():
            cells = row.locator("td")
            data[cells.nth(0).inner_text()] = cells.nth(1).inner_text()
        return data

    def close_modal(self):
        self.page.locator("#closeLargeModal").click()
