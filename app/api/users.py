

from fastapi import APIRouter, Depends
from app.db.database import get_async_db
from app.schemas.user_schema import UserCreate, UserOut
from app.crud.user_crud import create_user_async, get_user_by_id_async
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/", response_model=UserOut)
async def create_async_user_api(payload: UserCreate, db: AsyncSession = Depends(get_async_db)):
    return await create_user_async(db, payload)


@router.get("/{user_id}", response_model=UserOut)
async def get_async_user_by_id_api(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await get_user_by_id_async(db, user_id)
    return user