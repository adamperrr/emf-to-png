from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import os
import uuid

app = FastAPI(title="EMF to PNG Converter")

@app.post("/convert")
async def convert_emf_to_png(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".emf"):
        return JSONResponse(content={"error": "File must be .emf"}, status_code=400)

    input_path = f"/tmp/{uuid.uuid4()}.emf"
    output_path = input_path.replace(".emf", ".png")

    try:
        with open(input_path, "wb") as f:
            f.write(await file.read())

        subprocess.run(
            ["inkscape", input_path, "--export-type=png", "--export-filename", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return FileResponse(output_path, media_type="image/png", filename="converted.png")

    except subprocess.CalledProcessError as e:
        return JSONResponse(
            content={"error": f"Inkscape error: {e.stderr.decode()}"},
            status_code=500,
        )
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
