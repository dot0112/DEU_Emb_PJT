from openai import OpenAI
import os

api_key = os.getenv("APIKEY")


def request_openAI(korean_char):
    try:
        global api_key
        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            model="gpt-4o",
            store=True,
            messages=[
                {
                    "role": "system",
                    "content": """너는 한글의 자모음이 입력되면 이를 결합하여 적절한 한국어 문장으로 변환하여 결과를 보여야 해.  
번역된 모든 문장은 '/'으로 구분되며 끝나야해. "안녕하세요 반갑습니다"라는 결과에 대해서 "안녕하세요/반갑습니다/"라는 결과를 내야해   
자모음을 합칠 수 있는 경우에는 최대한 자연스러운 문장으로 완성해야 하며, 번역된 문장이 완전한 문장처럼 읽히는 경우 자모음을 추가로 분리하지 않아야 한다.  
만약 의미를 알 수 없는 자모음이 있을 경우, 해당 자모음을 분리해 뒤에 배치할 수 있다.  
예를 들어, "오늘 몸상태ㄴㅡㄴㅈㅗㅁㄱㅗㅐㄴㅊㅏㄴㅇㅡㅅㅣㄴㄱㅏㅇ"라는 입력이 주어질 경우, "오늘 몸상태는 좀 괜찮으신가요/"와 같이 번역 결과를 생성해야 한다.  
결과는 오직 번역된 문장만 포함하며 불필요한 설명은 하지 않는다. 주어진 자모음으로 문장을 만들었으나 중간에 남은 경우 이 자모음은 무시하고 결과에 추가하지 않는다.""",
                },
                {"role": "user", "content": f"{korean_char}"},
            ],
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
