import pandas as pd

sheets = pd.read_excel("2025_1(1차 수정).xlsx", sheet_name=None)

for sheet_name, df in sheets.items():
    print(f"\n📄 시트명: {sheet_name}")

    print("컬럼명 목록:", list(df.columns))

    print("컬럼명 타입:", {col: type(col).__name__ for col in df.columns})

    print("msg in columns ?", "msg" in df.columns)

    if "msg" in df.columns:
        print("msg 컬럼 dtype:", df["msg"].dtype)
        print("msg 컬럼 샘플:", df["msg"].head(3).tolist())
        print("send_date sample", df["send_date"].head(3).tolist())
        print("callback sample", df["callback"].head(3).tolist())
        print("mobile_no sample", df["mobile_no"].head(3).tolist())
        print("msg_type sample", df["msg_type"].head(3).tolist())
        print("result sample", df["result"].head(3).tolist())
