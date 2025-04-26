from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models   import ContatoDB, AgendamentoDB
from app.schemas.schemas import ContatoCreate, ContatoResponse, SMSSend
from twilio.rest import Client

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contatos/", response_model=ContatoResponse)
def create_contato(contato: ContatoCreate, db: Session = Depends(get_db)):
    db_contato = ContatoDB(nome=contato.nome, telefone=contato.telefone)
    db.add(db_contato)
    db.commit()
    db.refresh(db_contato)
    return db_contato

@router.get("/contatos/", response_model=list[ContatoResponse])
def get_contatos(db: Session = Depends(get_db)):
    return db.query(ContatoDB).all()

@router.get("/contatos/{contato_id}", response_model=ContatoResponse)
def get_contato(contato_id: int, db: Session = Depends(get_db)):
    db_contato = db.query(ContatoDB).filter(ContatoDB.id == contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return db_contato

@router.delete("/contatos/{contato_id}", response_model=ContatoResponse)
def delete_contato(contato_id: int, db: Session = Depends(get_db)):
    db_contato = db.query(ContatoDB).filter(ContatoDB.id == contato_id).first()
    if db_contato is None:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    
    db.delete(db_contato)
    db.commit()
    return db_contato

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

# Função para enviar a mensagem via Twilio
def send_sms(to: str, body: str):
    # Substitua os valores abaixo com as credenciais do Twilio
    account_sid = 123 # Insira seu SID de conta do Twilio
    auth_token =  123  # Insira seu token de autenticação do Twilio
    from_ = 123  # Insira seu número do Twilio

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=body,
        from_=from_,
        to=to
    )

    return message.sid

# Endpoint para testar o envio de uma mensagem SMS
@router.post("/send_sms/")
def send_test_sms(sms_data: SMSSend):
    try:
        message_sid = send_sms(
            to=sms_data.telefone,
            body=sms_data.mensagem
        )
        return {"status": "Mensagem enviada com sucesso!", "message_sid": message_sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")