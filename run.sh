#!/bin/bash
echo "Configurando ambiente..."

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado! Por favor, instale Python primeiro."
    exit 1
fi

# Cria venv se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa o venv
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Roda a aplicação
echo "Iniciando aplicação..."
python app.py