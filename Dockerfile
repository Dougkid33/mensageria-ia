FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /code

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY . .

# Exponha a porta
EXPOSE 8000
