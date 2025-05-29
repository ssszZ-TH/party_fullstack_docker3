from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.team import (
    create_team, get_team, get_all_teams,
    update_team, delete_team
)
from app.schemas.team import TeamCreate, TeamUpdate, TeamOut
from app.controllers.users.user import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/team", tags=["team"])

@router.post("/", response_model=TeamOut)
async def create_team_endpoint(team: TeamCreate, current_user: dict = Depends(get_current_user)):
    result = await create_team(team)
    if not result:
        logger.warning(f"ไม่สามารถสร้าง team")
        raise HTTPException(status_code=400, detail="ไม่สามารถสร้าง team")
    logger.info(f"สร้าง team: id={result.id}")
    return result

@router.get("/{team_id}", response_model=TeamOut)
async def get_team_endpoint(team_id: int, current_user: dict = Depends(get_current_user)):
    result = await get_team(team_id)
    if not result:
        logger.warning(f"ไม่พบ team: id={team_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ team")
    logger.info(f"ดึงข้อมูล team: id={result.id}")
    return result

@router.get("/", response_model=List[TeamOut])
async def get_all_teams_endpoint(current_user: dict = Depends(get_current_user)):
    results = await get_all_teams()
    logger.info(f"ดึงข้อมูล {len(results)} teams")
    return results

@router.put("/{team_id}", response_model=TeamOut)
async def update_team_endpoint(team_id: int, team: TeamUpdate, current_user: dict = Depends(get_current_user)):
    result = await update_team(team_id, team)
    if not result:
        logger.warning(f"ไม่สามารถอัปเดต team: id={team_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ team")
    logger.info(f"อัปเดต team: id={result.id}")
    return result

@router.delete("/{team_id}")
async def delete_team_endpoint(team_id: int, current_user: dict = Depends(get_current_user)):
    result = await delete_team(team_id)
    if not result:
        logger.warning(f"ไม่พบ team สำหรับลบ: id={team_id}")
        raise HTTPException(status_code=404, detail="ไม่พบ team")
    logger.info(f"ลบ team: id={team_id}")
    return {"message": "ลบ team เรียบร้อย"}