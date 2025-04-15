from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Contato(Base):
    __tablename__ = 'contatos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    telefone = Column(String, unique=True)

class Agendamento(Base):
    __tablename__ = 'agendamentos'
    id = Column(Integer, primary_key=True)
    contato_id = Column(Integer, ForeignKey("contatos.id"))
    horario_envio = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pendente")
