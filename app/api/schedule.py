from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import requests
import os
from app.db.session import SessionLocal
from app.models.models import AgendamentoDB
from fastapi import HTTPException
import logging
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para enviar a mensagem via UltraMsg
def send_sms_ultramsg(to: str, body: str):
    url = f"https://api.ultramsg.com/{os.getenv('INSTANCE_ID')}/messages/chat"
    token = os.getenv("ULTRAMSG_TOKEN")
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

# Função para buscar e enviar as mensagens agendadas
def send_scheduled_messages():
    db = SessionLocal()
    try:
        # Buscar agendamentos pendentes
        agendamentos = db.query(AgendamentoDB).filter(AgendamentoDB.status == "pendente").all()
        total_agendamentos = len(agendamentos)
        
        logger.info(f"Total de agendamentos pendentes: {total_agendamentos}")

        if total_agendamentos == 0:
            logger.info("Nenhum agendamento pendente encontrado.")
            return

        # Definir o fuso horário local (America/Sao_Paulo)
        local_tz = pytz.timezone("America/Sao_Paulo")
        local_time = datetime.now(local_tz)

        # Enviar as mensagens para cada agendamento
        for index, agendamento in enumerate(agendamentos, 1):
            # Converter o horário do banco (assumindo que está sem timezone e é horário local)
            db_time = agendamento.horario_envio
            
            # Se não tiver timezone, assumir que é o horário local
            if db_time.tzinfo is None:
                db_time_local = local_tz.localize(db_time)
            else:
                db_time_local = db_time.astimezone(local_tz)
            
            logger.info(f"Comparando horários: Banco de dados - {db_time_local}, Hora local - {local_time}")

            # Verificar se o horário de envio do agendamento já passou
            if db_time_local <= local_time:
                logger.info(f"Enviando agendamento {index} de {total_agendamentos}...")

                try:
                    logger.info(f"Enviando mensagem para {agendamento.contato.telefone} no horário: {local_time}")

                    # Enviar a mensagem
                    send_sms_ultramsg(agendamento.contato.telefone, agendamento.mensagem)

                    # Atualizar o status do agendamento
                    agendamento.status = "enviado"
                    db.commit()

                    logger.info(f"Mensagem enviada para {agendamento.contato.nome} com sucesso.")
                except Exception as e:
                    logger.error(f"Erro ao enviar mensagem para {agendamento.contato.nome}: {e}")
                    db.rollback()
            else:
                logger.info(f"O agendamento para {agendamento.contato.nome} ainda não chegou ao horário de envio (programado: {db_time_local}, atual: {local_time}).")
    except Exception as e:
        logger.error(f"Erro ao acessar o banco de dados: {str(e)}")
        db.rollback()
    finally:
        db.close()
# Função para iniciar o agendador
def start_scheduler():
    scheduler = BackgroundScheduler()
    # Agendar a função send_scheduled_messages para rodar a cada minuto
    scheduler.add_job(send_scheduled_messages, 'interval', minutes=1)
    scheduler.start()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
