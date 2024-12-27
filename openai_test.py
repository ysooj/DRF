from openai import OpenAI
from api_pjt.config import OPENAI_API_KEY
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

from openai import OpenAI
from api_pjt import config

CLIENT = OpenAI(
    api_key=config.OPENAI_API_KEY,
)



def ask_chatgpt(user_message):
    system_instructions = """
    이제부터 너는 '에이든 카페'의 직원이야.
    아래 종류의 음료 카테고리에서 주문을 받고, 주문을 처리하는 대화를 진행해.

    1. 아메리카노
    2. 카페라떼
    3. 프라푸치노
    4. 콜드브루
    5. 스무디

    주문을 받으면, 주문 내용을 확인하고, 주문을 처리하는 대화를 진행해.
    주문이 완료되면, 주문 내용을 확인하고, 주문이 완료되었음을 알려줘.
    """

    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_instructions,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
    )

    return completion.choices[0].message.content

while True:
    user_input = input("유저 : ")

    if user_input == 'exit':
        break

    response = ask_chatgpt(user_input)
    print("챗봇 : ", response, "\n\n")