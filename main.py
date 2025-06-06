from fastapi import FastAPI, File, UploadFile
import shutil
import os
import uuid
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Clarity Upscaler API is running!"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Create unique filenames
    input_filename = f"input_{uuid.uuid4().hex}.png"
    output_filename = f"output_{uuid.uuid4().hex}.png"

    # Save uploaded image
    with open(input_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run upscaler command (replace this with your real command)
    try:
        result = subprocess.run(
            ["python3", "clarity.py", input_filename, output_filename],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        return {"error": "Upscaling failed", "details": e.stderr}

    return {
        "message": "Upscaled successfully",
        "output_file": output_filename
    }
