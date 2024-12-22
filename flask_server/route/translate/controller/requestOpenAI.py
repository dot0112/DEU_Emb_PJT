from openai import OpenAI
import os

api_key = os.getenv("APIKEY")


def request_openAI(korean_char):
    try:
        global api_key
        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {
                    "role": "system",
                    "content": "너는 한글의 자모음이 들어오게 되면 이것을 적절한 한국어 문장으로 변환하여 결과를 보여야해. 너가 보여야 할 것은 결과 뿐 그 외에 특별한 말은 필요 없어",
                },
                {"role": "user", "content": f"{korean_char}"},
            ],
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
