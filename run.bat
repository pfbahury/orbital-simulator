@echo off
echo Configurando ambiente...

REM Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado! Por favor, instale Python primeiro.
    pause
    exit /b 1
)

REM Cria venv se não existir
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativa o venv
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instala dependências
echo Instalando dependências...
pip install -r requirements.txt

REM Roda a aplicação
echo Iniciando aplicação...
python app.py

pause