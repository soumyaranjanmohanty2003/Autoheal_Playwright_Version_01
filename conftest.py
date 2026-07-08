import pytest

from pages.practice_form_page import PracticeFormPage


@pytest.fixture
def practice_form_page(page):
    return PracticeFormPage(page)
