import zipfile
import os

# Recreate the final folder structure
final_folder = "/mnt/data/MSDChecklistApp_FinalComplete"
os.makedirs(final_folder, exist_ok=True)

# Final complete app code
app_code = '''
import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="근골격계 부담작업 체크리스트", layout="wide")
st.title("📋 근골격계 부담작업 체크리스트 시스템")

st.subheader("✅ 기본 정보 입력")
company = st.text_input("회사명")
department = st.text_input("부서명")
work_name = st.text_input("작업명")
unit_work = st.text_input("단위작업명")
writer = st.text_input("작성자")
write_date = st.date_input("작성일자", value=datetime.date.today())

memo_labels = {
    1: ["일일 해당작업시간:"],
    2: ["일일 해당작업시간:"],
    3: ["일일 해당작업시간:"],
    4: ["일일 해당작업시간:"],
    5: ["일일 해당작업시간:"],
    6: ["손가락으로 집는 물건의 용도와 이름:", "일일 해당작업시간:"],
    7: ["중량물의 명칭 및 무게:", "작업시간/작업횟수:"],
    8: ["25kg 이상 중량물의 명칭 및 무게:", "8시간 동안 드는 횟수:"],
    9: ["10kg 이상 중량물의 명칭 및 무게:", "8시간 동안 드는 횟수:"],
    10: ["4.5kg 이상 중량물의 명칭 및 무게:", "분당 횟수 및 해당작업의 작업시간:"],
    11: ["일일 해당작업시간:"],
    12: ["작업 설명 또는 기타 메모:"]
}

items = {
    1: "하루 4시간 이상 키보드 또는 마우스를 조작하는 작업",
    2: "2시간 이상 같은 동작을 반복하는 작업",
    3: "팔을 어깨 위로 드는 작업 등",
    4: "목이나 허리를 구부리거나 비트는 작업",
    5: "쪼그리거나 무릎을 굽힌 자세의 작업",
    6: "손가락으로 1kg 이상을 집는 작업",
    7: "한 손으로 4.5kg 이상 드는 작업",
    8: "25kg 이상 물체를 하루 10회 이상 드는 작업",
    9: "10kg 이상 물체를 무릎 아래, 어깨 위 등에서 드는 작업",
    10: "4.5kg 이상 물체를 분당 2회 이상 드는 작업",
    11: "손 또는 무릎으로 반복 충격을 가하는 작업",
    12: "기타 신체에 부담을 주는 작업"
}

responses = []
st.subheader("🧩 부담작업 항목 체크")
for i in range(1, 13):
    st.markdown(f"### {i}호. {items[i]}")
    applicable = st.radio(f"{i}호 해당 여부", ["예", "아니오"], key=f"item_{i}")
    count = st.number_input(f"{i}호 해당 인원 수", min_value=0, step=1, key=f"count_{i}")
    memos = []
    for idx, label in enumerate(memo_labels[i]):
        memos.append(st.text_input(label, key=f"memo_{i}_{idx}"))
    responses.append({
        "항목": f"{i}호",
        "해당": applicable,
        "인원": count,
        **{f"질문{j+1}": m for j, m in enumerate(memos)}
    })

st.subheader("💾 임시 저장")
if st.button("📥 .xlsx 파일로 임시 저장"):
    df = pd.DataFrame(responses)
    desc_df = pd.DataFrame({"작업내용": task_descriptions})
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="부담작업 체크")
        desc_df.to_excel(writer, index=False, sheet_name="작업내용")
    st.download_button(
        label="📂 temp_작성자명_날짜.xlsx 다운로드",
        data=buffer.getvalue(),
        file_name=f"temp_{writer}_{write_date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.info("※ Google Sheets에 저장하려면 Google 계정(Drive 권한)이 필요합니다. 인증 후 사용 가능합니다.")
'''

# Save app.py
with open(os.path.join(final_folder, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_code)

# Save requirements.txt
with open(os.path.join(final_folder, "requirements.txt"), "w") as f:
    f.write("streamlit\npandas\nxlsxwriter\n")

# Create zip archive
zip_path = "/mnt/data/MSDChecklistApp_FinalComplete.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for root, _, files in os.walk(final_folder):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, final_folder))

zip_path
