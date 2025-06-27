# chatbot/whatsapp/webhook.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from core.dependencies import get_db
from tenants.models import Tenant
from integrations.evolution_api import EvolutionAPI
from ia.processor import generate_response

router = APIRouter()
e = EvolutionAPI()

@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    body = await request.json()
    print("📨 Dados recebidos:", body)

    try:
        # Detecta se é o formato padrão da Meta (payload de teste real)
        if "entry" in body:
            changes = body["entry"][0]["changes"][0]["value"]
            message_obj = changes["messages"][0]
            contact = changes["contacts"][0]
            message = message_obj["text"]["body"]
            send_number = contact["wa_id"]
            instance = "instancia_teste"
            instance_key = "chave_teste"

        # Caso seja seu payload customizado com 'data'
        elif "data" in body:
            message = body["data"]["message"]["conversation"]
            instance = body["instance"]
            instance_key = body["apikey"]
            send_number = body["data"]["key"]["remoteJid"].split("@")[0]

        else:
            raise ValueError("Formato de payload não reconhecido.")

        print("📩 Mensagem recebida:", message)
        print("📱 Número do remetente:", send_number)
        print("🔐 API Key:", instance_key)

    except Exception as err:
        print("❌ Erro ao extrair dados do webhook:", err)
        return {"error": "Invalid payload format"}

    metadata = body["entry"][0]["changes"][0]["value"]["metadata"]
    phone_number_id = metadata["phone_number_id"]

    tenant = db.query(Tenant).filter(Tenant.phone_number_id == phone_number_id).first()

    if not tenant:
        print("⚠️ Tenant não encontrado para número:", send_number)
        print("🧪 Tipo do phone_number_id recebido:", type(phone_number_id))

        return {"error": "Tenant not found"}

    try:
        response = await generate_response(
            message=message,
            context_path=tenant.context_path,
            openai_key=tenant.openai_key,
        )
        resposta_ia = getattr(response, "content", str(response))
        print("🤖 Resposta da IA:", resposta_ia)
    except Exception as err:
        print("❌ Erro ao gerar resposta:", err)
        return {"error": "Erro ao gerar resposta com IA"}
    

    try:
        
        await e.enviar_mensagem(
            mensagem=resposta_ia,
            phone_number_id=tenant.phone_number_id,
            numero_destino=send_number,
        )


        print("✅ Mensagem enviada com sucesso.")
    except Exception as err:
        print("❌ Erro ao enviar mensagem via EvolutionAPI:", err)
        return {"error": "Erro ao enviar mensagem"}

    return {"response": message}


@router.get("/webhook")
async def verify(request: Request):
    print("📥 Recebido GET de verificação da Meta")
    """
    Endpoint de verificação exigido pelo WhatsApp Cloud API da Meta.
    """
    params = request.query_params
    VERIFY_TOKEN = "maycon_token"

    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == VERIFY_TOKEN
    ):
        return PlainTextResponse(content=params.get("hub.challenge"), status_code=200)

    return PlainTextResponse(content="Verificação falhou", status_code=403)
