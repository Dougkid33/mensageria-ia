from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base

class ContatoDB(Base):
    __tablename__ = 'contatos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    agendamentos = relationship('AgendamentoDB', back_populates='contato')

class AgendamentoDB(Base):
    __tablename__ = 'agendamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contato_id = Column(Integer, ForeignKey('contatos.id'), nullable=False)
    horario_envio = Column(DateTime, nullable=False)
    status = Column(String, default="pendente")
    mensagem = Column(String, nullable=False)  # Coluna para armazenar a mensagem

    # Relacionamento com o contato
    contato = relationship('ContatoDB', back_populates='agendamentos')