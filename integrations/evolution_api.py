import httpx

class EvolutionAPI:
    async def enviar_mensagem(self, mensagem, instance, instance_key, send_number):
        url = f'http://localhost:8080/message/sendText/{instance}'
        payload = {
            "number": send_number,
            "text": mensagem,
            "delay": 2000,
        }
        
        headers = {
            "apikey": instance_key,
            "Content-type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, headers=headers)
