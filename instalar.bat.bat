@echo off
echo ============================================
echo  Fleet Routing - Instalacao
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado.
    echo Baixe em: https://python.org/downloads
    echo Marque "Add Python to PATH" durante instalacao
    pause
    exit /b 1
)

echo [1/3] Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/3] Instalando dependencias...
pip install -r requirements.txt --quiet

echo [3/3] Verificando instalacao...
python -c "import fastapi; import sqlalchemy; import ortools; print('OK - tudo instalado!')"

echo.
echo ============================================
echo  Instalacao concluida!
echo  Proximo passo: edite o arquivo .env
echo  e execute: iniciar.bat
echo ============================================
pause
