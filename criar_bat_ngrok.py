conteudo = r"""@echo off
title Gelocrim Fleet Cloud
color 0A
echo.
echo  ================================================
echo   GELOCRIM FLEET CLOUD — Iniciando...
echo  ================================================
echo.
cd /d C:\fleet-cloud

:: Mata processos anteriores
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im ngrok.exe >nul 2>&1
timeout /t 2 >nul

:: Inicia o servidor FastAPI em janela separada
echo  [1/2] Iniciando servidor FastAPI...
start "Fleet API" cmd /k "cd /d C:\fleet-cloud && venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 4 >nul

:: Inicia ngrok em janela separada
echo  [2/2] Iniciando ngrok...
start "Ngrok Tunnel" cmd /k "ngrok http 8000"
timeout /t 3 >nul

:: Abre o browser
echo  Abrindo sistema...
start http://localhost:8000

echo.
echo  ================================================
echo   Sistema iniciado!
echo   - Web: http://localhost:8000
echo   - App: veja a URL na janela do Ngrok
echo  ================================================
echo.
pause
"""

with open(r'C:\fleet-cloud\iniciar_gelocrim.bat', 'w', encoding='utf-8') as f:
    f.write(conteudo)
print('iniciar_gelocrim.bat atualizado!')
