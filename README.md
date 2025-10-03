# Simulação de Órbitas

Uma aplicação web para simulação e visualização de órbitas planetárias e cometárias com animações interativas, os scripts de simulação orbital foram criadas pelo aluno de mestrado Thiago Marques da Silva.

**🔗 Código fonte:** [github.com/pfbahury/orbital-simulator](https://github.com/pfbahury/orbital-simulator)

## 📋 Requisitos

- Python 3.7 ou superior

## 🚀 Como Usar

### Opção 1: Executável (Mais Fácil - Recomendado)

**Para usuários que querem apenas usar a aplicação:**

1. Baixe o arquivo executável da seção [Releases](https://github.com/pfbahury/orbital-simulator/releases)
   - **Windows:** `OrbitaApp.exe`
   - **Linux/Mac:** `OrbitaApp`
2. Dê duplo clique no arquivo
3. Aguarde o navegador abrir automaticamente
4. Pronto! A aplicação estará rodando em `http://localhost:5000`

> **Nota:** O executável não precisa de Python instalado e funciona offline. Na primeira execução pode demorar alguns segundos para iniciar.

### Opção 2: Executar via Python (Para Desenvolvedores)

#### 1. Clone ou baixe o repositório

**Via Git:**
```bash
git clone https://github.com/pfbahury/orbital-simulator.git
cd orbital-simulator
```

**Via Download:**
Baixe o repositório clicando em "Code" → "Download ZIP" e extraia os arquivos.

#### 2. Criar ambiente virtual (recomendado)

```bash
python -m venv venv
```

#### 3. Ativar o ambiente virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

#### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

#### 5. Executar a aplicação

**Linux/Mac:**
```bash
python3 main.py
```

**Windows:**
```bash
python main.py
```

O navegador abrirá automaticamente em `http://localhost:5000`

### Opção 3: Docker

```bash
docker-compose up
```

Acesse: `http://localhost:5000`

## 🔨 Compilar o Executável (Para Desenvolvedores)

Se você quiser compilar o executável você mesmo:

**Windows:**
```bash
build.bat
```

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

O executável será gerado na pasta `dist/`

## 🛠️ Tecnologias Utilizadas

- Python (Flask)
- JavaScript (Plotly.js)
- HTML/CSS
- NumPy & SciPy
- PyInstaller (para executáveis)

## 📝 Licença

Este projeto está disponível como código aberto. Sinta-se livre para usar, modificar e distribuir.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests no [repositório do GitHub](https://github.com/pfbahury/orbital-simulator).

---

**⚠️ Nota sobre o Executável:** Alguns antivírus podem sinalizar o arquivo executável como suspeito. Isso é um falso positivo comum com aplicações PyInstaller. O código fonte está disponível para verificação no GitHub.