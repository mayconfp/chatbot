# chatbot/integrations/evolution_api.py

import httpx

from core.config import WHATSAPP_TOKEN

class EvolutionAPI:
    async def enviar_mensagem(self, mensagem, phone_number_id, numero_destino):
        url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "to": numero_destino if numero_destino.startswith("+") else f"+{numero_destino}",
            "type": "text",
            "text": {
                "body": mensagem
            }
        }

        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response_text = await response.aread()
            print("📤 Resposta Meta:", response.status_code, response_text.decode())
            response.raise_for_status()
