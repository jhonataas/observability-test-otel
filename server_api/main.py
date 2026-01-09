import logging
from fastapi import FastAPI, HTTPException
import httpx

from telemetry import setup_telemetry
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Inicializa OTel
setup_telemetry(service_name="server-api")

app = FastAPI(title="Server API")

FastAPIInstrumentor.instrument_app(app)

logger = logging.getLogger(__name__)

EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/users"


@app.get("/users")
async def get_users():
    logger.info("Recebida requisição /users")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(EXTERNAL_API_URL)
            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as exc:
        logger.exception("Erro ao chamar API externa")
        raise HTTPException(status_code=502, detail=str(exc))