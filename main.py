from fastapi import FastAPI, UploadFile, File
import pandas as pd
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    # 1️⃣ 验证文件类型
    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    # 2️⃣ 保存上传文件
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3️⃣ 读取 CSV
    df = pd.read_csv(file_path)

    # 4️⃣ 转成 JSON array
    data_array = df.to_dict(orient="records")

    # 5️⃣ 返回
    return {
        "filename": file.filename,
        "rows": len(data_array),
        "data": data_array
    }
