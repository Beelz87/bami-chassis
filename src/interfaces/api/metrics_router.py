from fastapi import APIRouter, Response
from src.infrastructure.monitoring.metrics import export_metrics

router = APIRouter()


@router.get("/metrics")
async def metrics():
    content_type, body = export_metrics()
    return Response(content=body, media_type=content_type)
