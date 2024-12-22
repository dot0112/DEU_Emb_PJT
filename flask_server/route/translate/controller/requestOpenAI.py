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
                    "content": "너는 한글의 자모음이 들어오게 되면 이것을 적절한 한국어 문장으로 변환하여 결과를 보여야해. 너가 보여야 할 것은 결과 뿐 그 외에 특별한 말은 필요 없어. 추가로 앞에 번역된 문장이 같이 들어올 것인데 이 문장과 이어서 번역하는 것도 가능해. 그리고 이렇게 한 경우 앞의 문장을 포함하여 답변하는 것이 가능해. 혹시 문장 뒤에 온 자모음이 너무 짧아 번역할 수 없다면 뒤에 '/'로 분리하여 자모음을 보내줘",
                },
                {"role": "user", "content": f"{korean_char}"},
            ],
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
