import logging
from fastapi import FastAPI, HTTPException
import httpx

from telemetry import setup_telemetry
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Inicializa OTel
setup_telemetry(service_name="client-api")

app = FastAPI(title="Client API")

FastAPIInstrumentor.instrument_app(app)

logger = logging.getLogger(__name__)

SERVER_API_URL = "http://server-api:8081/users"


@app.get("/getUsers")
async def get_users_from_server():
    logger.info("Chamando server-api")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(SERVER_API_URL)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as exc:
        logger.exception("Erro ao chamar server-api")
        raise HTTPException(status_code=502, detail=str(exc))