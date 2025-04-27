from pydantic import BaseModel
from datetime import datetime

class ContatoBase(BaseModel):
    nome: str
    telefone: str

class ContatoCreate(ContatoBase):
    pass

class ContatoResponse(ContatoBase):
    id: int
    
    class Config:
        from_attributes = True

class AgendamentoBase(BaseModel):
    contato_id: int
    horario_envio: datetime
    status: str = "pendente"
    mensagem: str 

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoResponse(AgendamentoBase):
    id: int
    
    class Config:
        from_attributes = True
        
class SMSSend(BaseModel):
    telefone: str
    mensagem: str        