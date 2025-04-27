Claro! Vou reformular o README, removendo as partes sobre o Twilio e aplicando as informações relevantes sobre o **UltraMsg**. Aqui está uma sugestão para o seu arquivo `README.md`:

---

# SMS API com UltraMsg

Este projeto é uma API em **FastAPI** para envio de mensagens via **UltraMsg**, utilizando **SQLAlchemy** para persistência de dados e **PostgreSQL** como banco de dados.

A API permite o cadastro de contatos, o envio de mensagens para os contatos cadastrados e o agendamento dessas mensagens para serem enviadas em um horário específico.

## Funcionalidades

- **Cadastro de contatos**: Adiciona contatos com nome e telefone.
- **Envio de SMS**: Envia mensagens para os contatos via **UltraMsg**.
- **Agendamento de SMS**: Permite agendar o envio de mensagens para um horário específico.

## Requisitos

- Python 3.9 ou superior.
- Docker (opcional, para rodar a aplicação e o banco de dados em contêineres).
- Uma conta no **UltraMsg** para o envio de mensagens via API.

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Dougkid33/mensageria-ia.git
cd mensageria-ia
```

### 2. Crie e ative um ambiente virtual

Se você ainda não tem um ambiente virtual, pode criar um com o comando abaixo:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Para Linux/MacOS
.venv\Scripts\activate     # Para Windows
```

### 3. Instale as dependências

Instale as dependências necessárias com o comando:

```bash
pip install -r requirements.txt
```

### 4. Configure o UltraMsg

Crie um arquivo `.env` na raiz do seu projeto com as seguintes variáveis:

```plaintext
ULTRAMSG_URL=https://api.ultramsg.com/instance116802/  # URL da sua instância UltraMsg
ULTRAMSG_TOKEN=seu_token_aqui  # Seu token de autenticação do UltraMsg
ULTRAMSG_NUMBER=seu_numero_aqui  # Número de WhatsApp da sua instância
```

Você pode obter esses dados ao criar uma conta no [UltraMsg](https://www.ultramsg.com/).

### 5. Rodando a aplicação

Para rodar a API, use o seguinte comando:

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível no `http://127.0.0.1:8000`.

## Endpoints

### 1. **Criar um novo contato**

**Método**: `POST`  
**URL**: `/contatos/`  
**Corpo da requisição**:

```json
{
  "nome": "João Silva",
  "telefone": "+5531998765432"
}
```

**Resposta**:

```json
{
  "id": 1,
  "nome": "João Silva",
  "telefone": "+5531998765432"
}
```

### 2. **Obter todos os contatos**

**Método**: `GET`  
**URL**: `/contatos/`  

**Resposta**:

```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "telefone": "+5531998765432"
  },
  ...
]
```

### 3. **Obter um contato específico**

**Método**: `GET`  
**URL**: `/contatos/{contato_id}`  

**Resposta**:

```json
{
  "id": 1,
  "nome": "João Silva",
  "telefone": "+5531998765432"
}
```

### 4. **Deletar um contato**

**Método**: `DELETE`  
**URL**: `/contatos/{contato_id}`  

**Resposta**:

```json
{
  "id": 1,
  "nome": "João Silva",
  "telefone": "+5531998765432"
}
```

### 5. **Enviar SMS**

**Método**: `POST`  
**URL**: `/send_sms/`  

**Corpo da requisição**:

```json
{
  "telefone": "+5531998765432",
  "mensagem": "Sua mensagem aqui"
}
```

**Resposta**:

```json
{
  "status": "Mensagem enviada com sucesso!",
  "result": {
    "message": "Mensagem enviada com sucesso"
  }
}
```

## Como funciona o envio de SMS

O envio de SMS é feito através da API **UltraMsg**. Ao chamar o endpoint `/send_sms/`, a aplicação envia uma mensagem para o número de telefone informado utilizando a API da UltraMsg.

### Função `send_sms_ultramsg`

```python
def send_sms_ultramsg(to: str, body: str):
    url = os.getenv("ULTRAMSG_URL") + "messages/chat"
    token = os.getenv("ULTRAMSG_TOKEN")
    from_ = os.getenv("ULTRAMSG_NUMBER")

    payload = {
        "token": token,
        "to": to,
        "body": body
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return response.json()  # Retorna a resposta da API UltraMsg
    else:
        raise Exception(f"Erro ao enviar mensagem: {response.text}")
```

A função `send_sms_ultramsg` utiliza os dados do `.env` para enviar a mensagem para o número fornecido, e a resposta da API é retornada.

## Contribuição

Sinta-se à vontade para contribuir com melhorias no projeto! Você pode abrir uma **pull request** ou sugerir melhorias através de issues.

---
