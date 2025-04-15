

# **Mensageria Inteligente com IA**

Este é um projeto em andamento para criar um **serviço de mensageria inteligente** que usa **Inteligência Artificial (IA)** para gerar e enviar mensagens SMS automaticamente para contatos específicos em horários programados.

## **Tecnologias Utilizadas**

- **Python**: Linguagem de programação principal.
- **FastAPI**: Framework para criar APIs rápidas e eficientes.
- **SQLAlchemy**: ORM para trabalhar com banco de dados PostgreSQL.
- **PostgreSQL**: Banco de dados relacional para armazenar dados.
- **Twilio**: Serviço para enviar SMS para os contatos.
- **OpenAI GPT-3**: Inteligência Artificial para gerar conteúdo dinâmico e personalizado para as mensagens.
- **APScheduler**: Biblioteca para agendar o envio das mensagens.
- **Docker**: Containerização da aplicação para garantir portabilidade e consistência no ambiente de desenvolvimento e produção.

## **Objetivo**

O projeto visa automatizar a comunicação via SMS, permitindo que os usuários agendem o envio de mensagens com conteúdo personalizado, gerado por **Inteligência Artificial**. Ele permite o envio de mensagens para contatos específicos em horários programados.

## **Funcionalidades**

1. **Geração de Mensagens com IA**: O sistema utiliza um modelo de IA (OpenAI GPT-3) para gerar o conteúdo das mensagens de forma dinâmica e personalizada.
2. **Envio de SMS**: As mensagens geradas são enviadas para os contatos utilizando o serviço **Twilio**.
3. **Agendamento**: O usuário pode agendar a mensagem para ser enviada em um horário específico usando o **APScheduler**.
4. **Persistência de Dados**: O serviço mantém o histórico de mensagens e agendamentos no banco de dados **PostgreSQL**.
5. **API RESTful**: A aplicação disponibiliza endpoints para interagir com o sistema, permitindo agendar mensagens e consultar o status.

## **Como Rodar o Projeto Localmente**

### **Pré-requisitos**

- **Python 3.12** ou superior
- **Docker** e **Docker Compose** para containerização (opcional, mas recomendado)

### **1. Clonando o Repositório**

Clone este repositório para a sua máquina local:

```bash
git clone https://github.com/Dougkid33/mensageria-ia.git
cd mensageria-ia
```

### **2. Criando um Ambiente Virtual**

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Para Linux/Mac
.venv\Scripts\activate     # Para Windows
```

### **3. Instalando Dependências**

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

### **4. Configurando o Banco de Dados**

O projeto utiliza o **PostgreSQL** para persistir dados. As credenciais de acesso ao banco de dados devem ser configuradas nas variáveis de ambiente ou diretamente no código.

Você pode usar o **Docker** para rodar o PostgreSQL facilmente com o comando:

```bash
docker-compose up --build
```

Isso irá levantar o banco de dados PostgreSQL e a aplicação.

### **5. Rodando a Aplicação**

Para rodar a aplicação localmente, use o comando:

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível em `http://127.0.0.1:8000`.

### **6. Testando a API**

Após rodar a aplicação, você pode acessar a **documentação interativa** da API em `http://127.0.0.1:8000/docs`, que é gerada automaticamente pelo FastAPI.

## **Como Usar**

1. **Agendar uma Mensagem**: Utilize o endpoint `POST /agendar_sms/` para enviar uma solicitação para o envio de SMS. Você deve fornecer o número de telefone, o horário de envio e o tipo de mensagem que deseja enviar.
   
2. **Geração de Mensagens com IA**: O conteúdo da mensagem será gerado automaticamente com IA (usando OpenAI GPT-3).

3. **Receber Status**: O status do envio das mensagens pode ser consultado via API.

## **Desenvolvimento Futuro**

- **Implementação de novas funcionalidades** de personalização de mensagens.
- **Integração com mais serviços de envio de SMS**, além do Twilio.
- **Melhoria no agendamento e no gerenciamento de mensagens**.

## **Licença**

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
