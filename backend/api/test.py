import asyncio
from websockets import connect
import json

# Exemplo de token (caso use JWT)
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNzg5NzU5LCJpYXQiOjE3NTE3ODI1NTksImp0aSI6IjI4YTViYzUyNWRiODRiYzQ4YWJiNDY1OGU4MzE4MzA4IiwidXNlcl9pZCI6MSwiaXNzIjoiemFiZS1hcGkifQ.QRQ52xrU0lHjkNxq5gziGLrdJNeUBT6vfnOtkizIVrg"

async def test_ws():
    uri = "ws://127.0.0.1:8000/ws/core/"
    
    # Cabeçalhos se você usa JWT na autenticação
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }

    async with connect(uri, extra_headers=headers) as websocket:
        print("✅ Conectado com sucesso")

        # Enviando mensagem JSON
        await websocket.send(json.dumps({
            "type": "algum_tipo_de_mensagem",
            "payload": {
                "chave": "valor"
            }
        }))

        # Recebendo resposta (opcional)
        resposta = await websocket.recv()
        print("📨 Resposta do servidor:", resposta)

asyncio.run(test_ws())
