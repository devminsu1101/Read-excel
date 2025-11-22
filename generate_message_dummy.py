import pandas as pd
import random
from datetime import datetime, timedelta
import os 

# ============================
# 1) 더미 데이터 설정
# ============================

NUM_ROWS = 1000   # 생성할 메시지 개수
RESULT_CHOICES = ["S", "F"] # 문자 전송 성공/실패
MESSAGE_TYPES = ["SMS", "LMS", "MMS"]

# 강의명
course_name_file = 'course_names.txt'
if not os.path.isfile(course_name_file): 
    raise FileNotFoundError(f"강의명 파일 없음: {course_name_file}")

with open(course_name_file, "r", encoding="utf-8") as file: 
    COURSE_NAMES = [line.strip() for line in file if line.strip()]

# 메시지 내용
base_message_template = """
[고객지원 무료교육 안내]
저희 교육기관에서는 소상공인 고객을 대상으로 무료교육을 운영하고 있습니다. 
▶교육내용 : {keywords} 
▶교육비용 : 전액무료
▶안내 및 신청 : https://forms.gle/ABCDE12345
(무료수신거부 080-000-0000)
"""


# ============================
# 2) 더미 데이터 생성 함수
# ============================

def generate_dummy_row():
    send_date = datetime(2025, 2, 3, 14, 5, 10) + timedelta(seconds=random.randint(0, 5000))
    callback = "01-2345-6789"
    mobile_no = "010-" + str(random.randint(0000, 9999)) + "-" + str(random.randint(0000, 9999)) # 보내는 번호 랜덤 설정
    message_type = random.choice(MESSAGE_TYPES)
    result = random.choice(RESULT_CHOICES)

    # 메시지에 키워드 삽입 (한 메시지 안에 여러 교육을 홍보하는 것을 가정)
    num_keywords = random.randint(1, 3)
    keywords = random.sample(COURSE_NAMES, num_keywords)
    keywords_str = " / ".join(keywords)
    message = base_message_template.format(keywords=keywords_str).strip()

    return {
        "send_date": send_date,
        "callback": callback,
        "mobile_no": mobile_no,
        "message_type": message_type,
        "result": result,
        "message": message
    }


# ============================
# 3) 실제 데이터프레임 구성
# ============================

rows = [generate_dummy_row() for _ in range(NUM_ROWS)]
df = pd.DataFrame(rows)


# ============================
# 4) 엑셀 저장
# ============================

output_file = "dummy_raw_messages.xlsx"
df.to_excel(output_file, index=False)

print(f"📁 더미 엑셀 생성 완료: {output_file}")
print(f"총 {NUM_ROWS}개의 메시지를 생성했습니다!")
