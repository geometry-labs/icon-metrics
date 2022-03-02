from typing import List

import aiohttp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from icon_metrics.api.db import get_session
from icon_metrics.config import settings
from icon_metrics.http_client import http_client
from icon_metrics.models.metrics import NodeState, Supply

router = APIRouter()


@router.get("/metrics/supply")
async def get_supply(session: AsyncSession = Depends(get_session)) -> Supply:
    """Get latest supply."""
    result = await session.execute(select(Supply).order_by(Supply.timestamp.desc()).limit(1))
    supply = result.first()
    return supply[0]


@router.get("/metrics/node-state")
async def get_node_state(
    http_client: aiohttp.ClientSession = Depends(http_client), network_name: str = "mainnet"
) -> List[NodeState]:
    """Get node state."""
    r = await http_client.post(
        settings.ICON_NODE_URL + "/api/v3/query",
        params={"query": f'icon_prep_node_state{{network_name="{network_name}"}}'},
    )

    if r.status == 200:
        metrics = await r.json()

        processed_metrics = []
        for i in metrics["data"]["result"]:
            processed_metrics.append(
                NodeState(prep_name=i["metric"]["name"], state_id=i["value"][1])
            )

        return processed_metrics
    else:
        # TODO: Make fallback call to DB
        raise HTTPException(status_code=503, detail="Prometheus service unavailable")
