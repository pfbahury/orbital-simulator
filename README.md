# Simulação de Órbitas

Uma aplicação web para simulação e visualização de órbitas planetárias e cometárias com animações interativas.

## 📋 Requisitos

- Python 3.7 ou superior

## 🚀 Instalação

### Opção 1: Clone via Git
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### Opção 2: Download direto
Baixe o repositório diretamente do GitHub clicando no botão "Code" → "Download ZIP" e extraia os arquivos.

## ⚙️ Configuração

### 1. Criar ambiente virtual (recomendado)
```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual
**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

## ▶️ Execução

**Linux/Mac:**
```bash
python3 app.py
```

**Windows:**
```bash
python app.py
# ou
py app.py
```

Após executar o comando, abra seu navegador e acesse `http://localhost:5000` para usar a aplicação.

## Alternativa utilizando arquivos de scripts automático

## Windows
1. Clique duas vezes em `run.bat`
2. Aguarde o setup automático
3. Acesse: http://localhost:5000

## Linux/Mac
1. Execute: `chmod +x run.sh && ./run.sh`
2. Acesse: http://localhost:5000

## Com Docker
1. Execute: `docker-compose up`
2. Acesse: http://localhost:5000

## 🛠️ Tecnologias Utilizadas

- Python (Flask)
- JavaScript (Plotly.js)
- HTML/CSS
- NumPy & SciPy
