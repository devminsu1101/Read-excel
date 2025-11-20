import pandas as pd

# 엑셀 파일 로드
file = "2025교육일정.xlsx"
df = pd.read_excel(file)

# '수료인원', '만족도' 숫자로 변환 (문자가 섞여 있을 경우)
df['수료인원'] = pd.to_numeric(df['수료인원'], errors='coerce').fillna(0).astype(int) # 수료인원은 정수
df['만족도'] = pd.to_numeric(df['만족도'], errors="coerce").fillna(0).astype(float) # 만족도는 float

# 과정명별로 그룹화 후 차수 순서대로 정렬
grouped = df.sort_values(by=['차수']).groupby('과정명')

for course_name, group in grouped:
    print(f"\n📌 과정명: {course_name}")
    
    # 아직 진행하지 않은 그룹 제외
    filtered_group = group[group['만족도'] > 0]

    # 차수별 수료인원 출력
    for idx, row in filtered_group.iterrows():
        print(f"  차수 {row['차수']} : {row['수료인원']:,}명, 만족도 : {row['만족도']:,.2f}") # 숫자 뒤에 :, 를 붙이면 세 자리별로 쉼표를 찍어줌  / # 숫자 뒤에 :.2f를 붙이면 소수점 두 자리까지 보여줌 
    
    # 과정별 총합
    total = filtered_group['수료인원'].sum()
    print(f"  ✅ 총 수료인원: {total:,}명")

    # 만족도 높은/낮은 차수 정리 
    high_score = filtered_group[filtered_group['만족도'] >= 4.90]
    low_score = filtered_group[filtered_group['만족도'] < 4.50]

    print("  ⭐ 만족도 4.90 이상 차수:")
    if not high_score.empty:
        for idx, row in high_score.iterrows():
            print(f"    - {row['차수']:,.0f} 차 (만족도 {row['만족도']:,.2f})")
    else: 
        print("    == 없음 == ")

        # 만족도 4.50 미만
    print("  ⚠ 만족도 4.50 미만 차수:")
    if not low_score.empty:
        for idx, row in low_score.iterrows():
            print(f"    - {row['차수']:,.0f} 차 (만족도 {row['만족도']:,.2f})")
    else: 
        print("    == 없음 == ")
        