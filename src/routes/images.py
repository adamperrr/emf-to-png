from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
import subprocess
import os
import uuid
from ..utils.files import remove_file

router = APIRouter(prefix="/images", tags=["images"])

@router.post("/convert-emf-to-png")
async def convert_emf_to_png(file: UploadFile = File(...)):
    """
    Convert an uploaded EMF file to PNG using Inkscape.

    Args:
        file (UploadFile): The uploaded EMF file.
    Returns:
        FileResponse: The converted PNG file or JSONResponse in case of error.
    """

    if not file.filename.lower().endswith(".emf"):
        print("[ERROR] Uploaded file is not an EMF file")
        return JSONResponse(content={"error": "File must be .emf"}, status_code=400)

    input_path = f"/tmp/{uuid.uuid4()}.emf"
    output_path = input_path.replace(".emf", ".png")

    print(f"[INFO] Starting conversion for file: {file.filename}")
    print(f"[INFO] Input path: {input_path}")
    print(f"[INFO] Output path: {output_path}")

    try:
        content = await file.read()
        with open(input_path, "wb") as f:
            f.write(content)
        input_size = os.path.getsize(input_path)
        print(f"[INFO] Input file saved ({input_size} bytes)")

        print(f"[INFO] Running Inkscape...")
        result = subprocess.run(
            ["inkscape", input_path, "--export-type=png", "--export-filename", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"[INFO] Inkscape stdout:\n{result.stdout.decode()}")
        print(f"[INFO] Inkscape stderr:\n{result.stderr.decode()}")

        if os.path.exists(output_path):
            output_size = os.path.getsize(output_path)
            print(f"[INFO] Output file generated ({output_size} bytes)")
        else:
            print("[ERROR] Output file was not created")
            return JSONResponse(content={"error": "Conversion failed, output file not found"}, status_code=500)

        return FileResponse(
            output_path,
            media_type="image/png",
            filename="converted.png",
            background=BackgroundTask(lambda: remove_file(input_path) or remove_file(output_path))
        )

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Inkscape returned an error: {e.stderr.decode()}")
        return JSONResponse(
            content={"error": f"Inkscape error: {e.stderr.decode()}"},
            status_code=500,
        )
