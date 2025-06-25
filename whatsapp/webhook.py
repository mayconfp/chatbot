# chatbot/whatsapp/webhook.py

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from core.dependencies import get_db  # ✅ novo
from tenants.models import Tenant
from integrations.evolution_api import EvolutionAPI
from ia.processor import generate_response

router = APIRouter()
e = EvolutionAPI()

@router.post("/webhook")  # não esquecer o decorator!
async def webhook(
    request: Request,
    db: Session = Depends(get_db)  # ✅ injeta o banco automaticamente
):
    data = await request.json()
    message = data['data']['message']['conversation']
    instance = data['instance']
    instance_key = data['apikey']
    send_number = data['data']['key']['remoteJid'].split('@')[0]

    tenant = db.query(Tenant).filter(Tenant.whatsapp_number == send_number).first()
    if not tenant:
        return {'error': 'Tenant not found'}

    response = await generate_response(
        message=message,
        context_path=tenant.context_path,
        openai_key=tenant.openai_key,
    )

    await e.enviar_messagem(response.content, instance, instance_key, send_number)
    return {'response': message}
