@echo off
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)
call venv\Scripts\activate
echo Instalando/Atualizando dependencias...
pip install -r requirements.txt
python main.py
pause