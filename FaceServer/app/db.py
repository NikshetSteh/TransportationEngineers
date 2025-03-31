from typing import Annotated

import chromadb
from chromadb.api import AsyncClientAPI
from config import get_config
from fastapi import Depends

chroma_client: AsyncClientAPI | None = None


async def get_chroma_db() -> AsyncClientAPI:
    global chroma_client

    if chroma_client is not None:
        return chroma_client

    config = get_config()
    chroma_client = await chromadb.AsyncHttpClient(
        host=config.CHROMA_DB_HOST, port=config.CHROMA_DB_PORT
    )
    return chroma_client


ChromaDependency = Annotated[AsyncClientAPI, Depends(get_chroma_db)]
