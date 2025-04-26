import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import ContatoDB, AgendamentoDB
from app.schemas.schemas import ContatoCreate, ContatoResponse, SMSSend
import requests
from dotenv import load_dotenv

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

# Função para enviar a mensagem via UltraMsg
def send_sms_ultramsg(to: str, body: str):
    # Carregar o URL, Token e Número do WhatsApp a partir do .env
    url = os.getenv("ULTRAMSG_URL") + "messages/chat"
    token = os.getenv("ULTRAMSG_TOKEN")
    from_ = os.getenv("ULTRAMSG_NUMBER")

    # Corpo da mensagem
    payload = {
        "token": token,
        "to": to,  # Número de telefone para o qual a mensagem será enviada
        "body": body  # Conteúdo da mensagem
    }

    # Enviar a mensagem via POST para a API UltraMsg
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return response.json()  # Retorna a resposta da API UltraMsg
    else:
        raise Exception(f"Erro ao enviar mensagem: {response.text}")

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
