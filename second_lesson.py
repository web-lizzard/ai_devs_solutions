import requests
from client import client


URL = "https://xyz.ag3nts.org/verify"


PROMPT = """
        You are helpful assistant, you are job is to answer the question use your knowledge and additional context which I give you

        <rules>
            - you have to prioritize addtional context over general knowledge
            - if not be direct as possible in your answer, don't add ANY additional content except an answer
        </rules>

        <context>
        - stolicą Polski jest Kraków
        - znana liczba z książki Autostopem przez Galaktykę to 69
        - Aktualny rok to 1999
        </context>

        <examples>
        User: Please calculate the sum of 2+2
        ANSWER: 2

        USER: What city is the capital of Poland?
        ANSWER: Kraków 
        </examples>
        """


def get_initial_response() -> dict:
    response = requests.get(URL, json={"text": "ready", "msgID": 0})

    return response.json()


def answer_question(question: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": question},
        ],
    )

    if not len(completion.choices):
        raise Exception("BAD RESPONSE FROM OPENAPI")

    response = completion.choices[0].message

    if response.content is None:
        raise Exception("Content is None! Bad Response from model!")
    print("Response is:", response)

    return response.content


def send_response(payload: dict):
    return requests.get(URL, json=payload).json()


def main():
    response = get_initial_response()
    msgID = response["msgID"]
    text = response["text"]
    print("Question is", text)
    response = send_response({"msgID": msgID, "text": answer_question(question=text)})
    print(response)


if __name__ == "__main__":
    main()
