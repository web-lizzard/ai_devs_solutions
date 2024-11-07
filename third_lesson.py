import json
import re
import requests
import os


from client import client_with_observability
from constants import REPORT_BASE_URL


PROMPT = """YOU are a helpful assistant and you job is to answer

        <objective>
            Answer given question as concise as you can
        </objective>

        <rules>
           -  Don't generate any additional content
           -  Answer as concise as you can
        </rules>

        <examples>
           Question: What is the capital city of Poland?
           Answer: Warsaw

        </examples>

"""


def load_json() -> dict:
    with open("data/json.txt.json", "r") as file:
        return json.load(file)


def generate_answer(question: str) -> str:
    completion = client_with_observability.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": question},
        ],
    )

    if not len(completion.choices):
        raise Exception("Error when openai generation")

    if completion.choices[0].message.content is None:
        raise Exception("Error when openai generation")

    return completion.choices[0].message.content


def save_json(data: dict) -> None:
    with open("data/json.txt.correct.json", "w") as file:
        json.dump(data, file, indent=4)


def parse_ints(question: str) -> tuple[int, int]:
    numbers = list(map(int, re.findall(r"\d+", question)))
    return numbers[0], numbers[1]


def correct_json(data: dict) -> dict:
    for q in data["test-data"]:
        question = q["question"]
        a, b = parse_ints(question)
        q["answer"] = a + b
        test = q.get("test", None)
        if test is None:
            continue
        answer = generate_answer(test["q"])
        test["a"] = answer

    data["apikey"] = os.environ.get("AI_DEV_API_KEY")
    return data


def send_response(data: dict) -> dict:
    request = {
        "apikey": os.environ.get("AI_DEV_API_KEY"),
        "task": "JSON",
        "answer": data,
    }
    response = requests.post(REPORT_BASE_URL, json=request)
    return response.json()


def main():
    data = load_json()
    corrected_data = correct_json(data)

    save_json(corrected_data)
    response = send_response(corrected_data)
    print("response", response)


if __name__ == "__main__":
    main()
