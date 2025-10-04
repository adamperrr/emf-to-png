# emf-to-png

Simple FastAPI endpoint converting EMF to PNG using Inkscape

## Running the app

```bash
docker build -t emf2png-poetry .

docker run -p 8000:8000 emf2png-poetry
```

## Converting EMF images to PNG

```bash
curl -X POST -F "file=@test.emf" http://localhost:8000/convert -o result.png
```