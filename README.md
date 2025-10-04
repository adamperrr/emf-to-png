# emf-to-png

Simple FastAPI service that converts EMF to PNG using Inkscape

## Running the app

```bash
docker build -t emf2png .

docker run -p 8000:8000 emf2png
```

## Converting EMF images to PNG

```bash
curl -X POST -F "file=@sample1.emf" http://localhost:8000/convert -o result.png
```