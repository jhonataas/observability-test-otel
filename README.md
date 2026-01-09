# Observability Test – OpenTelemetry (Python)

## Objetivo
Demonstrar observabilidade distribuída em Python usando OpenTelemetry, incluindo traces, logs, métricas e propagação de contexto.

## Arquitetura
client-api → server-api → external API

(OTLP → OpenTelemetry Collector)

## Stack
- FastAPI + Uvicorn
- Httpx (async)
- OpenTelemetry SDK (Python)
- OTLP (gRPC)
- OpenTelemetry Collector
- Docker / Docker Compose

## Observabilidade
- **Traces**: instrumentação automática (FastAPI + Httpx)
- **Logs**: exportados via OTLP com `trace_id` e `span_id`
- **Métricas**: métricas HTTP automáticas
- **Contexto**: propagação W3C (`traceparent`) end-to-end

## Collector
- Receivers: OTLP (gRPC/HTTP)
- Processors: `memory_limiter`, `resource`, `batch`
- Resource: `deployment.environment=challenge-test`
- Exporter: `logging` (debug)

## Execução
```bash
docker-compose up --build
```
Acesse:
```bash
http://localhost:8080/getUsers
```

## Validação
- Trace único cobrindo toda a requisição
- Logs correlacionados com spans
- Traces, logs e métricas visíveis no Collector

## Nota sobre Desenvolvimento
Para otimizar o tempo de implementação deste desafio, utilizei ferramentas de IA Generativa (LLMs) como apoio na criação do *boilerplate* inicial da infraestrutura (Dockerfiles e estrutura base das APIs).

Toda a lógica crítica de **Observabilidade**, incluindo a escolha das bibliotecas de instrumentação, configuração da propagação de contexto (Context Propagation) e a definição dos processadores do Collector, foi implementada e auditada manualmente para garantir as boas práticas atuais do OpenTelemetry.