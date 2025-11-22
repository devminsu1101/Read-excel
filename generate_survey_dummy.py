import pandas as pd
import numpy as np
import random
import os

# ---------------------------------------
# 1) 가상의 과정명 & 장소명 설정
# ---------------------------------------

# course_name 불러오기 
course_name_file = 'course_names.txt'
if not os.path.isfile(course_name_file): 
    raise FileNotFoundError(f"강의명 파일 없음: {course_name_file}")

with open(course_name_file, "r", encoding="utf-8") as file: 
    COURSE_NAMES = [line.strip() for line in file if line.strip()]

PLACES = [
    "네오컨벤션센터",
    "브릿지타워 세미나실",
    "루미너스 교육센터",
    "이카루스 그랜드볼룸",
    "이노베이션홀 세미나룸",
    "라이트하우스 컨퍼런스룸",
    "파크빌딩 교육실",
    "더플래닛 러닝스페이스",
    "코스모스연수원",
    "씨티포럼 아카데미홀"
]

# ---------------------------------------
# 2) 공통 문항 + 개별 문항 시스템
# ---------------------------------------
COMMON_QUESTIONS = [
    "1. 과정에 대한 전반적인 만족도",
    "2. 강사의 전문성",
    "3. 강의 내용의 명확성",
    "4. 강의 자료의 적절성",
    "5. 교육 내용의 실용성",
    "6. 프로그램 전반 구성",
    "7. 시설 및 환경 만족도",
    "8. 식사 만족도",
]

COURSE_SPECIFIC_QUESTIONS = {
    "디지털 문제해결 역량 향상 과정": ["9. 실습 난이도", "10. 실습 장비 만족도"],
    "고객 중심 서비스 커뮤니케이션 과정": ["9. 롤플레잉 유익성"],
    "미래형 비즈니스 전략 워크숍": ["9. 비즈니스 사례 적절성", "10. 그룹토의 효과성"],
    "데이터 기반 의사결정 실무 과정": ["9. 데이터 활용 난이도"],
    "창의적 프로젝트 기획 & 실행 과정": ["9. 아이디어 발산 활동 유익성"],
    "소셜미디어 운영 실전 마스터": ["9. 실습 플랫폼 적절성", "10. 장비 편의성"],
    "AI 활용 업무 자동화 과정": ["9. 자동화 실습 난이도"],
    "비즈니스 보고서 작성 및 스토리텔링 과정": ["9. 실습 과제 난이도", "10. 예시 자료 유용성"],
    "직무 생산성 향상 부트캠프": ["9. 개인별 피드백 만족도"],
    "조직 협업 및 갈등관리 실습 과정": ["9. 팀 활동 유익성", "10. 갈등 해결 실습 적절성"]
}

# -----------------------------
# 3) 더미 데이터 생성 함수
# -----------------------------
def generate_course_sheet(course_name, num_batches=10): # 한 과정당 10차
    """
    각 과정별 raw data 시트를 생성.
    하나의 과정 내에 N차수가 존재하며,
    각 차수는 25~30명의 참여자 데이터를 생성.
    """

    data = []
    possible_locations = random.sample(PLACES, num_batches)

    # 문항 구성: 공통 + 과정별 문항
    questions = COMMON_QUESTIONS.copy()
    if course_name in COURSE_SPECIFIC_QUESTIONS:
        questions += COURSE_SPECIFIC_QUESTIONS[course_name]

    # 각 차수 생성
    for batch in range(1, num_batches + 1):
        num_people = random.randint(25, 30)
        location = possible_locations[batch - 1]

        for _ in range(num_people):
            row = {
                "과정명": course_name,
                "차수": batch,
                "날짜": f"2025-0{batch}-15",
                "장소": location,
            }

            # 각 문항 점수(1~5 정수)
            for question in questions:
                row[question] = random.randint(1, 5)

            data.append(row)

    return pd.DataFrame(data)


# -----------------------------
# 4) 전체 엑셀 생성
# -----------------------------
def create_dummy_excel(filename="dummy_raw_survey_data.xlsx"):

    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        for course in COURSE_NAMES:
            df = generate_course_sheet(course)
            df.to_excel(writer, sheet_name=course[:31], index=False)

    print(f"더미 Raw 데이터 생성 완료 → {filename}")


# -----------------------------
# 실행
# -----------------------------
if __name__ == "__main__":
    create_dummy_excel()
