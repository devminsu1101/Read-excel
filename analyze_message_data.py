import pandas as pd
import os

# 분석할 엑셀 파일 리스트
excel_files = [
    "dummy_raw_messages.xlsx",
]
# 데이터에서 메시지를 의미하는 칼럼의 지정
message_column = 'message'

# course_name.txt에서 강의명 읽기
course_name_file = "course_names.txt"
if not os.path.isfile(course_name_file): # 파일이 없을 경우
    raise FileNotFoundError(f"강의명 파일 없음: {course_name_file}")

with open(course_name_file, "r", encoding="utf-8") as file: # course_name_file 을 utf-8 방식으로 인코딩해서 '읽는다("r" : read, 읽기 모드)
    course_names = [line.strip() for line in file if line.strip()] # 텍스트 파일의 한 라인 전체를 강의명로 해서 읽는다. 

print(f"🔑 읽은 강의명: {course_names}\n") # 어떤 강의명들을 읽었는지 확인

# 강의명별 총합
keyword_counts = {kw: 0 for kw in course_names} # dict 방식, 각 속성에 접근하기 쉬워 유용

# 전체 메시지 개수 (확인차 설정)
total_count = 0 
total_successed_count = 0 # S 메시지 개수
total_failed_count = 0 # F 메시지 개수
matched_total_count = 0 # 문자 내에서 강의명를 찾은 횟수

for file in excel_files:
    if not os.path.isfile(file): # 분석할 파일 리스트의 이름과 일치하는 파일이 없으면
        print(f"⚠ 파일 없음: {file}") 
        continue

    print(f"\n📂 파일 분석중: {file}")
    sheets = pd.read_excel(file, sheet_name=None) # sheet_name=None : sheet 구분 없이 excel을 읽겠다. // 엑셀 자체를 sheet 라는 변수에 담아 해당 반복문에서 사용한다. 

    for sheet_name, df in sheets.items(): 
    # df == DataFrame : 엑셀의 시트를 그대로 담은 표 객체. sheet 자체를 의미 (pandas에서는 하나의 DataFrame을 df라는 변수로 받음)
        print(f"  🔍 시트: {sheet_name}")

        if message_column not in df.columns or "result" not in df.columns: # df.colums에서 msg 컬럼과 result 컬럼의 여부를 확인 
            print("    ⚠ msg 또는 result 컬럼 없음 - 건너뜀")
            continue 

        # result가 S인 행만
        df_s = df[df["result"] == "S"] # result가 S인 행(문자가 성공적으로 전송된)의 데이터를 의미 
        df_f = df[df["result"] == "F"]

        total_count += df.shape[0]
        total_successed_count += df_s.shape[0] # 전체 성공한(S) msg의 개수 (문자가 보내진 개수)
        total_failed_count += df_f.shape[0] 

        print(f"    📌 S 메시지 개수: {df_s.shape[0]:,}개")
        print(f"    ⚠ F 메시지 개수: {df_f.shape[0]:,}개")

        # 강의명 집계
        for kw in course_names:
            count = df_s[message_column].astype(str).str.contains(kw, na=False).sum() 
            # .astype(str) : msg 컬럼의 값을 문자열로 설정 (숫자/None이어도 문자열로 변환) > 문자열 검색을 안전하게 하기 위해 
            # str.contains(kw) : 각 문자들 중에 keyword(kw)가 들어있는지 확인하고 True/False 리스트 반환(na=False : NaN이면 False로 처리함)
            # 한 문자를 가지고 kw 개수만큼 반복을 도는데 해당 kw가 한 문자에 몇 개 들어있는지 확인하고, 그걸 더한 값을 저장함 
            keyword_counts[kw] += count
            matched_total_count += count

# 누락 메시지 개수
# unmatched_count = total_successed_count - matched_total_count

# 최종 결과 출력
print("\n===========================")
print("📌 전체 종합 결과 (S 메시지 기준)")
print("===========================\n")

print(f"전체 S 메시지 행 개수: {total_successed_count:,}개")
print(f"F 메시지 총 개수: {total_failed_count:,}개")
print(f"S, F가 명시되지 않은 메시지 행 개수 : {total_count - total_successed_count:,}개 - F 메시지 총 개수와 같아야 함")
print(f"강의명 매칭된 개수 총합: {matched_total_count:,}개")
# print(f"❗ 강의명에 걸리지 않은 메시지: {unmatched_count:,}개\n")

print("🔎 강의명별 총합")
for kw, count in keyword_counts.items():
    print(f"{kw} : {count:,}개")