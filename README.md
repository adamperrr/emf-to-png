# emf-to-png

Simple endpoint for converting EMF images to PNG format

## Requirements

python >= 3.11
poetry >= 2.2

## Running the app using Docker

```bash
docker build -t emf2png .
docker run -p 8000:8000 emf2png
```

## Local environment

```bash
poetry run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

## Converting EMF images to PNG

```bash
curl -X POST -F "file=@sample1.emf" http://localhost:8000/images/convert-emf-to-png -o result.png
```