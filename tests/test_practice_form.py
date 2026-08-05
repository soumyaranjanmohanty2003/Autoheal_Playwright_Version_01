"""
Scenario: Submit the DemoQA Practice Form and verify the confirmation
modal reflects the data that was entered.
"""


def test_practice_form_submission(practice_form_page):
    student = {
        "first_name": "Soumya",
        "last_name": "Mohanty",
        "email": "soumya.test@example.com",
        "gender": "Male",
        "mobile": "9876543210",
        "day": "15",
        "month": "May",
        "year": "1998",
        "subject": "Maths",
        "hobbies": ["Sports", "Reading"],
        "address": "221B Baker Street, Kolkata",
        "state": "NCR",
        "city": "Delhi",
    }

    practice_form_page.open()
    practice_form_page.fill_name(student["first_name"], student["last_name"])
    practice_form_page.fill_email(student["email"])
    practice_form_page.select_gender(student["gender"])
    practice_form_page.fill_mobile(student["mobile"])
    practice_form_page.set_date_of_birth(student["day"], student["month"], student["year"])
    practice_form_page.add_subject(student["subject"])
    practice_form_page.select_hobbies(student["hobbies"])
    practice_form_page.fill_current_address(student["address"])
    practice_form_page.select_state_and_city(student["state"], student["city"])
    practice_form_page.submit()

    assert practice_form_page.get_modal_title() == "Thanks for submitting the form"

    modal_data = practice_form_page.get_modal_data()
    full_name = f"{student['first_name']} {student['last_name']}"
    assert modal_data["Student1 Name"] == full_name
    assert modal_data["Student Email"] == student["email"]
    assert modal_data["Gender"] == student["gender"]
    assert modal_data["Mobile"] == student["mobile"]
    assert modal_data["Date of Birth"] == f"{student['day']} {student['month']},{student['year']}"
    assert modal_data["Subjects"] == student["subject"]
    assert modal_data["Hobbies"] == ", ".join(student["hobbies"])
    assert modal_data["Address"] == student["address"]
    assert modal_data["State and City"] == f"{student['state']} {student['city']}"
