@echo off
echo ============================================
echo  Fleet Routing - Iniciando servidor
echo ============================================
echo.

if not exist venv (
    echo ERRO: Execute primeiro instalar.bat
    pause
    exit /b 1
)

if not exist .env (
    echo ERRO: Arquivo .env nao encontrado.
    echo Copie .env.example para .env e preencha os dados.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Iniciando API em http://localhost:8000
echo Pressione Ctrl+C para parar
echo.
start "Fleet Worker" cmd /k "call venv\Scripts\activate.bat && celery -A app.celery_worker worker --loglevel=warning --concurrency=2 -Q routing"
timeout /t 3 /nobreak >nul
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
