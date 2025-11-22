import pandas as pd

file = "dummy_raw_messages.xlsx" # 살펴보고싶은 파일 이름 설정 
sheets = pd.read_excel(file, sheet_name=None)

for sheet_name, df in sheets.items():
    print(f"\n📄 시트명: {sheet_name}\n")

    print("컬럼명 목록:", ', '.join(list(df.columns)))

    print("컬럼명 타입:", {col: type(col).__name__ for col in df.columns})

    print(f"message in columns ?", "msg" in df.columns) # msg 컬럼이 있는지 확인

    if "msg" in df.columns:
        print("msg 컬럼 dtype:", df["msg"].dtype)
        print("msg 컬럼 샘플:", df["msg"].head(3).tolist())