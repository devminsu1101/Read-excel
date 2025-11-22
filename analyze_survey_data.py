import pandas as pd
import os
import re

# 1. 변수 설정
# 1-1. 불러올 파일 설정 
file = "dummy_raw_survey_data.xlsx"
if not os.path.isfile(file) : 
  raise FileNotFoundError(f"{file} 파일 없음")

# 1-2. 파일 내 각각의 시트에 접근
sheets = pd.read_excel(file, sheet_name=None) # 파일 내 여러 시트를 읽고 싶다면! 'sheet_name=None'
# 1-3. 이후 프린트할 결과 저장용 
overall_results = {}
# 추가) 만족도 높은 차수와 낮은 차수 분리해 출력
HIGH_SCORE = 4.5
LOW_SCORE = 4.0

# 2. 파일 탐색 

for sheet_name, df in sheets.items(): 
    print(f"현재 탐색중인 시트 : {sheet_name}\n")

    # 2-1. 모든 문항을 float로 변환 
    # df_numeric = df.copy() 
    # df_numeric = df_numeric.apply(pd.to_numeric, errors="ignore")

    # 2-2. 1번 문항 이름 찾기 
    question1_col = next((col for col in df.columns if "1." in str(col)))
    if question1_col is None : 
        print(f"'1번 문항을 찾을 수 없습니다.")
        continue 
    
    # 2-3. 요구사항 1) 차수별 1번 문항 만족도 조사 
    # 2-3-1. '차수' 문항 확인 
    if '차수' not in df.columns: 
        print("'차수' 칼럼이 없습니다.")
        continue
    df['차수'] = pd.to_numeric(df['차수'], errors='coerce')
    
    # 2-3-2. 
    grouped = df.groupby("차수")[question1_col].mean()

    # 2-3-3. 
    print('차수별 1번 문항(전반적 만족도) 평균 : ')
    for chasu, score in grouped.items(): 
        print(f" - {int(chasu)}차 : {score:.2f}")

    # 만족도 높은/낮은 차수 확인 
    high_chasu = grouped[grouped >= HIGH_SCORE]
    low_chasu = grouped[grouped < HIGH_SCORE]

    print(f"\n🔹 평균 >= {HIGH_SCORE}점 이상 차수:")
    if not high_chasu.empty:
        for chasu, score in high_chasu.items():
            print(f" - {int(chasu)}차 : {score:.2f}")
    else:
        print(" - 없음")

    print(f"\n🔹 평균 < {LOW_SCORE}점 이하 차수:")
    if not low_chasu.empty:
        for chasu, score in low_chasu.items():
            print(f" - {int(chasu)}차 : {score:.2f}")
    else:
        print(" - 없음")

    # 2-4. 요구사항 2) 각 문항별 전체 평균 조사 
    # 2-4-1. 문항 컬럼 탐색해서 "n. "형태 포함된 컬럼 찾기 
    question1_cols = [col for col in df.columns if re.match(r'^\d+\.', str(col).strip())]
    if not question1_cols: 
        print(" 문항 컬럼이 없음 ")
        continue

    # 2-4-2. 숫자로 변환 가능한 문항만 필터 
    df[question1_cols] = df[question1_cols].apply(pd.to_numeric, errors='coerce')

    # 2-4-3. 각 과정 평균 계산 
    means = df[question1_cols].mean()


    print("\n")
    print(" 각 문항별 평균 만족도 : \n")
    for col, value in means.items(): 
        print(f" - {col} : {value:.2f}")

    print("\n")