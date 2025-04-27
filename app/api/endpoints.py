import os
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import ContatoDB, AgendamentoDB
from app.schemas.schemas import ContatoCreate, ContatoResponse, SMSSend, AgendamentoCreate, AgendamentoResponse
import requests
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis do arquivo .env
load_dotenv()

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para enviar a mensagem através do UltraMsg
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
        return response.json()
    else:
        raise Exception(f"Erro ao enviar mensagem: {response.text}")

# Função de envio agendado (executa em segundo plano)
def send_scheduled_message(agendamento_id: int, db: Session):
    # Consultar o agendamento no banco
    agendamento = db.query(AgendamentoDB).filter(AgendamentoDB.id == agendamento_id).first()

    if agendamento is None:
        raise Exception(f"Agendamento {agendamento_id} não encontrado")

    if agendamento.status != "pendente":
        return  # Se o agendamento já foi enviado ou está cancelado, não faz nada

    # Enviar a mensagem
    result = send_sms_ultramsg(
        to=agendamento.contato.telefone,  # Pega o telefone do contato associado
        body=agendamento.mensagem
    )

    # Atualiza o status do agendamento
    agendamento.status = "enviado"
    db.commit()

    return result

# Endpoint para agendar o envio de mensagens
@router.post("/schedule_message/{agendamento_id}")
def schedule_message(agendamento_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Adiciona o envio da mensagem em segundo plano
    background_tasks.add_task(send_scheduled_message, agendamento_id, db)
    return {"message": "Mensagem agendada com sucesso."}

# Endpoint para testar o envio de uma mensagem SMS com UltraMsg
@router.post("/send_sms/")
def send_test_sms(sms_data: SMSSend):
    try:
        # Envia a mensagem SMS usando o UltraMsg
        result = send_sms_ultramsg(
            to=sms_data.telefone,
            body=sms_data.mensagem
        )
        return {"status": "Mensagem enviada com sucesso!", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")

# Endpoint para criar um novo contato
@router.post("/contatos/", response_model=ContatoResponse)
def create_contato(contato: ContatoCreate, db: Session = Depends(get_db)):
    db_contato = ContatoDB(nome=contato.nome, telefone=contato.telefone)
    db.add(db_contato)
    db.commit()
    db.refresh(db_contato)
    return db_contato

# Endpoint para obter todos os contatos
@router.get("/contatos/", response_model=list[ContatoResponse])
def get_contatos(db: Session = Depends(get_db)):
    return db.query(ContatoDB).all()

# Endpoint para obter um contato específico
@router.get("/contatos/{contato_id}", response_model=ContatoResponse)
def get_contato(contato_id: int, db: Session = Depends(get_db)):
    db_contato = db.query(ContatoDB).filter(ContatoDB.id == contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return db_contato

# Endpoint para deletar um contato
@router.delete("/contatos/{contato_id}", response_model=ContatoResponse)
def delete_contato(contato_id: int, db: Session = Depends(get_db)):
    db_contato = db.query(ContatoDB).filter(ContatoDB.id == contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    
    db.delete(db_contato)
    db.commit()
    return db_contato

# Endpoint para atualizar um contato
@router.put("/contatos/{contato_id}", response_model=ContatoResponse)
def update_contato(contato_id: int, contato: ContatoCreate, db: Session = Depends(get_db)):
    db_contato = db.query(ContatoDB).filter(ContatoDB.id == contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    
    db_contato.nome = contato.nome
    db_contato.telefone = contato.telefone
    db.commit()
    db.refresh(db_contato)
    return db_contato

# Endpoint para criar um novo agendamento
@router.post("/agendamentos/", response_model=AgendamentoResponse)
def create_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db)):
    # Verificar se o contato existe no banco de dados
    db_contato = db.query(ContatoDB).filter(ContatoDB.id == agendamento.contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")

    # Criando o agendamento com a mensagem
    db_agendamento = AgendamentoDB(
        contato_id=agendamento.contato_id,
        horario_envio=agendamento.horario_envio,
        status=agendamento.status,
        mensagem=agendamento.mensagem  # Adiciona a mensagem no agendamento
    )

    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)

    return db_agendamento
