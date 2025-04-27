from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Obtém a URL do banco de dados a partir do .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Criação do engine para se conectar ao banco de dados
engine = create_engine(DATABASE_URL)

# Criação da base para os modelos
Base = declarative_base()

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {str(e)}")
    finally:
        db.close()
