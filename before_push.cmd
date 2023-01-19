@echo off
cls
docker-compose down -t 2

@rem 7z a "tomita-parser-binaries.7z" -mmt16 -mx9 -m9=LZMA2 PythonApp/tomita_runnable/libmystem_c_binding.so PythonApp/tomita_runnable/tomita-parser.exe PythonApp/tomita_runnable/tomita-parser

@rem del /s /q "python_temp.7z"
@rem 7z a -t7z "python_temp.7z" -mmt8 -mx9 -m9=LZMA2 "PythonApp/temp/"
@rem del /s /q "mongodb_data.7z"
@rem 7z a -t7z "mongodb_data.7z" -mmt8 -mx9 -m9=LZMA2 "mongodb_data/"

del /s /q "mongodb_and_models.7z"
7z a -t7z "mongodb_and_models.7z" -mmt8 -mx9 -m9=LZMA2 "mongodb_data/" "PythonApp/temp/"

pause
