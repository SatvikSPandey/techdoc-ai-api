from fastapi import Depends
from app.core.security import verify_api_key


async def common_dependencies(api_key: str = Depends(verify_api_key)) -> str:
    return api_key