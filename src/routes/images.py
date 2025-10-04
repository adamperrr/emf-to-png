from fastapi import APIRouter, File, UploadFile, Query
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
import subprocess
import os
import uuid
from ..utils.files import remove_file
from ..utils.logger import get_logger

logger = get_logger("routes.images")

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/convert-emf-to-png")
async def convert_emf_to_png(
    file: UploadFile = File(...),
    width: int | None = Query(None, description="Optional output width in pixels"),
    height: int | None = Query(None, description="Optional output height in pixels"),
):
    """
    Convert an uploaded EMF file to PNG using Inkscape.

    Args:
        file (UploadFile): The uploaded EMF file.
    Returns:
        FileResponse: The converted PNG file or JSONResponse in case of error.
    """

    error_response = await _validate_parameters(file, width, height)
    if error_response:
        return error_response

    input_path = f"/tmp/{uuid.uuid4()}.emf"
    output_path = input_path.replace(".emf", ".png")

    logger.info(f"Input path: {input_path}")
    logger.info(f"Output path: {output_path}")
    logger.info(f"Requested resize: width={width}, height={height}")

    logger.info(f"Starting conversion for file: {file.filename}")
    
    try:
        content = await file.read()
        with open(input_path, "wb") as f:
            f.write(content)
        input_size = os.path.getsize(input_path)
        logger.info(f"Input file saved ({input_size} bytes)")

        command = _prepare_inkscape_command(input_path, output_path, width, height)

        logger.info(f"Executing: {' '.join(command)}")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in iter(process.stdout.readline, ''):
            logger.info(line.strip())
        for line in iter(process.stderr.readline, ''):
            logger.warning(line.strip())

        return_code = process.wait()
        if return_code != 0:
            logger.error(f"Inkscape process exited with code {return_code}")
            return JSONResponse(
                content={"error": "Inkscape error: see logs for details"},
                status_code=500,
            )

        if os.path.exists(output_path):
            output_size = os.path.getsize(output_path)
            logger.info(f"Output file generated ({output_size} bytes)")
        else:
            logger.error("Output file was not created")
            return JSONResponse(
                content={"error": "Conversion failed, output file not found"},
                status_code=500
            )

        return FileResponse(
            output_path,
            media_type="image/png",
            filename="converted.png",
            background=BackgroundTask(lambda: remove_file(input_path) or remove_file(output_path))
        )

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return JSONResponse(
            content={"error": "Unexpected error occurred, see logs for details"},
            status_code=500,
        )


async def _validate_parameters(file: UploadFile, width: int | None, height: int | None) -> JSONResponse | None:
    if file.content_type != "image/emf":
        return JSONResponse(
            content={"error": "Invalid file type, only EMF files are supported"},
            status_code=400,
        )

    if not file.filename.lower().endswith(".emf"):
        logger.error("Uploaded file is not an EMF file")
        return JSONResponse(content={"error": "File must be .emf"}, status_code=400)

    header = await file.read(4)
    await file.seek(0)  # Reset file pointer after reading
    if header != b'\x01\x00\x00\x00':
        return JSONResponse(
            content={"error": "Invalid EMF file (bad header)"}, 
            status_code=400
        )

    if height is not None and (not isinstance(height, int) or height <= 0):
        return JSONResponse(
            content={"error": "Height must be a positive integer"},
            status_code=400,
        )

    if width is None and height is None:
        return JSONResponse(
            content={"error": "At least one of width or height must be specified"},
            status_code=400,
        )

    return None


def _prepare_inkscape_command(input_path: str, output_path: str, width: int | None, height: int | None) -> list[str]:
    command = ["inkscape", input_path, "--export-type=png", "--export-filename", output_path]

    if width is not None:
        command += ["--export-width", str(width)]
    if height is not None:
        command += ["--export-height", str(height)]

    return command