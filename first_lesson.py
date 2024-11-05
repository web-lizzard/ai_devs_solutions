import requests
from bs4 import BeautifulSoup
from prompts.first_lesson_prompt import PROMPT
from client import client


# URL of the page you want to scrape
PAGE_URL = "https://xyz.ag3nts.org/"


def parse_page() -> None:
    text = get_home()
    soup = BeautifulSoup(text, "html.parser")
    question = find_question(soup)
    response = submit_form(soup, question=question)
    save_file_from_response(response)


def answer_question(question: str | None) -> int:
    if question is None:
        return -1

    content = (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": question},
            ],
        )
        .choices[0]
        .message.content
    )

    if content is None:
        return -1

    return int(content)


def get_home() -> str:
    response = requests.get(PAGE_URL)
    response.raise_for_status()

    return response.text


def find_question(soup: BeautifulSoup) -> str | None:
    human_question = soup.find("p", id="human-question")
    human_question_content = (
        human_question.get_text(strip=True) if human_question else None
    )
    print(f"Human Question Content: {human_question_content}")

    return human_question_content


def submit_form(soup: BeautifulSoup, question: None | str) -> str:
    form = soup.find("form")
    if not form:
        raise Exception()

    # Define values to fill in the form
    form_data = {
        "username": "tester",
        "password": "574e112a",
        "answer": answer_question(question=question),
    }

    # Prepare the form data by updating with user-provided values for matching fields
    target_names = {"username", "password", "answer"}
    inputs = form.find_all(
        "input", attrs={"name": lambda name: name in target_names if name else False}
    )
    for input_field in inputs:
        input_name = input_field.get("name")
        if input_name in form_data:
            input_field["value"] = form_data[input_name]
            form_data[input_name] = input_field["value"]

    # Submit the form
    form_action = form.get("action")
    submit_url = (
        form_action if form_action.startswith("http") else PAGE_URL + form_action
    )
    response = requests.post(submit_url, data=form_data)
    response.raise_for_status()

    print("Form submitted")
    return response.text


def save_file_from_response(response: str) -> None:
    soup = BeautifulSoup(response, "html.parser")

    download_link = soup.find("a", href="/files/0_13_4b.txt")
    if download_link:
        file_url = download_link["href"]
        file_url = file_url if file_url.startswith("http") else PAGE_URL + file_url

        # Download the file
        file_response = requests.get(file_url)
        file_response.raise_for_status()  # Check if the request was successful

        # Save the downloaded file
        with open("data/0_13_4b.txt", "wb") as file:
            file.write(file_response.content)
        print("File downloaded successfully.")


if __name__ == "__main__":
    parse_page()
