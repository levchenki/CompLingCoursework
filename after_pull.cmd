@echo off
cls
docker-compose down -t 2

7z x -aos "tomita-parser-binaries.7z"

rd /s /q "mongodb_data/"
rd /s /q "PythonApp/temp/"
7z x "mongodb_and_models.7z"

pause
