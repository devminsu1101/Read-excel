import pandas as pd
import os
import re

# 1. 변수 설정
# 1-1. 불러올 파일 설정 
file = "2025년 노란우산 고객지원 교육 만족도 조사 결과.xlsx"
if not os.path.isfile(file) : 
  raise FileNotFoundError(f"{file} 파일 없음")
# 1-2. 파일 내 각각의 시트에 접근
sheets = pd.read_excel(file, sheet_name=None) # 파일 내 여러 시트를 읽고 싶다면! 'sheet_name=None'
# 1-3. 이후 프린트할 결과 저장용 
overall_results = {}

# 2. 파일 탐색 

for sheet_name, df in sheets.items(): 
    print(f"현재 탐색중인 시트 : {sheet_name}\n")

    # 2-1. 모든 문항을 float로 변환 
    # df_numeric = df.copy() 
    # df_numeric = df_numeric.apply(pd.to_numeric, errors="ignore")

    # 2-2. 1번 문항 이름 찾기 
    question1_col = None  
    for col in df.columns: 
        if "1." in str(col) and "전반적인 만족도" in str(col): 
            question1_col = col 
            break
    if question1_col is None : 
        print("'1. 전반적인 만족도' 문항을 찾을 수 없습니다.")
        continue 
    
    # 2-3. 요구사항 1) 차수별 1번 문항 만족도 조사 
    # 2-3-1. '차수' 문항 확인 
    if '차수' not in df.columns: 
        print("'차수' 칼럼이 없습니다.")
        continue
    
    # 2-3-2. 
    df['차수'] = pd.to_numeric(df['차수'], errors='coerce')
    grouped = df.groupby("차수")[question1_col].mean()

    # 2-3-3. 
    for chasu, score in grouped.items(): 
        print(f" - {int(chasu)}차 : {score:.2f}")

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
    print(" 각 문항별 평균 만족도 : ")
    for col, value in means.items(): 
        print(f" - {col} : {value:.2f}")

    print("\n\n")