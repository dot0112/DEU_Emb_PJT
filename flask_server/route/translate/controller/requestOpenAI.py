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
                    "content": """너는 한글의 자모음이 입력되면 이를 결합하여 적절한 한국어 문장으로 변환하여 결과를 보여야 해.
                    너는 결과만 보여주고, 그 외의 불필요한 말은 포함하지 않아야 한다.
                    추가로, 번역된 문장이 앞에 포함되어 있을 경우 이를 이어서 번역하는 것도 가능하다.
                    이 경우, 앞의 문장을 포함하여 자연스럽게 이어진 결과를 작성해야 한다.
                    만약 자모음이 너무 짧아서 번역할 수 없거나 의미를 알 수 없는 경우, 해당 자모음을 앞 문장에서 분리하여 '/' 뒤에 배치해야 한다.
                    예를 들어, "안녕하세요 나는 ㄱㅣㅁㅗㅎ" 같은 입력이 주어질 경우, 결과는 "안녕하세요. 나는/ㄱㅣㅁㅗㅎ"와 같이 처리해야 한다.""",
                },
                {"role": "user", "content": f"{korean_char}"},
            ],
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
