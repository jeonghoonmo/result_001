import os
#from PIL import Image
#import pytesseract
import openai

# Step 1: OCR to extract text from images
#def extract_text_from_images(folder_path):
#    all_text = ""
#    for filename in os.listdir(folder_path):
#        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
#            image_path = os.path.join(folder_path, filename)
#            text = pytesseract.image_to_string(Image.open(image_path), lang='kor')  # Change to Korean OCR
#            all_text += text + "\n"
#    return all_text

# Step 1: OCR to extract text from solar(layout api)
import requests

api_key = "up_5Hwhgm3F0QaJdjsAxu3rMJkcSoLnU"
filename = "./수학경시_초4_결과지.pdf"

url = "https://api.upstage.ai/v1/document-ai/layout-analysis"
headers = {"Authorization": f"Bearer {api_key}"}
files = {"document": open(filename, "rb")}
response = requests.post(url, headers=headers, files=files)
all_text = response.json()

# "mimetype" 이후의 내용만 추출
def get_text_after_mimetype(data):
    found_mimetype = False
    result = {}

    for key, value in data.items():
        if found_mimetype:
            result[key] = value
        if key == "mimetype":
            found_mimetype = True

    return result

extracted_text = get_text_after_mimetype(all_text)
#print(text_after_mimetype)

#extracted_text = "화랑초등학교 수학경시대회 결과지\n응시자 ID 040101 @hr2311 응시 지역 응시일\n학교 화랑초등학교 학년 4 이름 권민경\n나의 점수 확인\n원점수 (내점수 : 68 점) 백점환산\n분석구분\n배점 내점수 내점수환산 학년평균\n이해 24 24 100 95.2\n계산 20 20 100 89.5\n문제해결력 20 12 60 57.9\n추론 36 12 33.3 70.1\n나의 위치 그래프 수학 내용영역\n100 내점수 전체평균 상위10%\n100\n90\n90\n80\n80\n70\n70\n60\n60\n50\n50\n40\n40\n30\n30\n20 20\n10 10\n0 0\n내점수 전체평균 상위 10% 수와 연산 도형 측정\n수학 행동영역 인지적영역 평가\n내점수 전체평균 상위10%\n내점수 전체평균 상위10%\n100 이해 100 A(지식)\n60\n40 40\n20 20\n추론 0 계산 서답형 0 B(이해)\n문제해결력 C(적용)\n본 콘텐츠의 저작권은 제공처 또는 한국교육평가센터에 있으며, 이를 무단 이용하는 경우 저작권법 등에 따라 법적책임을 질 수 있습니다.\n화랑초등학교 수학경시대회 결과지\n개인 정오표\n번호 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n답안 3 3 3 2 3 5 4 2 5 4 2 1 1 3 2\n정답 3 3 3 2 3 5 2 2 5 4 2 3 1 3 2\n채점결과 0 0 O 0 0 O X 0 O O 0 X 0 O O\n정답률 100 78.82 91.76 90.58 97.64 98.82 34.11 97.64 96.47 90.58 90.58 51.76 94.11 84.70 100\n번호 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30\n답안 0 3 4 2 4 4 0 0 4 0\n정답 3 3 4 1 2 서답형 서답형 서답형 서답형 서답형\n채점결과 X 0 O X X O X X 0 X\n정답률 91.76 89.41 82.35 55.29 89.41 40 57.64 74.11 62.35 5.882\n나의 성취도 지수\n성취도 수학 학습 역량\nA Ⓑ C D E A B C Ⓓ E\n각 단원에서 학습한 개념과 원리를 활용하여 기본적인 수학적 개념을 정확히 이해하는 학습 활동을 진행하여\n응용문제를 해결할 수 있으며 수학 교과의 학업성취도는 문제에서 요구하는 지식이 무엇인지 파악하는 능력을\n우수한 편입니다. 문제 풀이할 때 집중력을 높이고 키워야 합니다. 문장제 문제를 여러 가지 방법으로\n지시문에 주어진 조건을 분석하여 문제 해결의 실마리를 해결해 나가는 학습을 진행하고 틀린 문제를 고쳐 푸는\n찾고, 풀이 과정을 서술하는 훈련을 통해 실수를 오답노트의 활용도 좋은 학습 방법이 될 것입니다.\n줄이도록 노력해야 합니다.\n※서답형 답안 표기는 학생의 점수 입니다.\n서울여자대학교 부설\n한국교육평가센터 화랑 화 랑 초 등 학 교\nKorea Center For Education Evaluation HWARANG ELEMENTARY SCHOOL\n본 콘텐츠의 저작권은 제공처 또는 한국교육평가센터에 있으며, 이를 무단 이용하는 경우 저작권법 등에 따라 법적책임을 질 수 있습니다."

# Step 2: Integrate with OpenAI API using ChatGPT-4
def analyze_with_chatgpt(api_key, extracted_text):
    openai.api_key = api_key  # Use the actual key here
    
    request_prompt = f"""
    선생님이 학생의 수학 시험 결과를 학부모님께 설명한다고 가정해 봅시다. 
    1)학생이 잘한 점, 부족했던 점, 그리고 앞으로 개선이 필요한 점에 대해 자세히 설명해주세요.
    2)문제 번호는 1번에서 25번까지 있으며, 문제의 난이도는 1번부터~25번 순으로 쉬운 것부터 어려운 것으로 진행됩니다. 
      학생의 난이도별 정답/오답 분석(1번~10번, 11번~20번,21번~25번)하고, 
    3)향후 학습 계획에 대해 조언해 주세요.
    
    학생의 수학성적 결과분석: 
    {extracted_text}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 수학 시험 결과를 분석하는 유용한 도우미입니다."},
            {"role": "user", "content": request_prompt}
        ]
    )
    
    return response['choices'][0]['message']['content']

# Step 3: Main execution
if __name__ == "__main__":
    # 실제 OpenAI API 키를 여기에 입력해야 합니다
    OPENAI_API_KEY = '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' 
    
    # 결과 시트 이미지가 있는 폴더 경로를 정의합니다
    # folder_path = "./result/"
    
    # 폴더 내 모든 이미지에서 텍스트를 추출합니다
    # extracted_text = extract_text_from_images(folder_path)
    
    if extracted_text:
        # 추출한 텍스트를 사용해 ChatGPT로 분석합니다
        analysis_result = analyze_with_chatgpt(OPENAI_API_KEY, extracted_text)
        print("OCR추출:시작\n")
        print(extracted_text)
        #print("OCR추출:끝\n")
        
        print("분석 결과:\n")
        print(analysis_result)
    else:
        print("제공된 이미지에서 텍스트를 찾을 수 없습니다.")