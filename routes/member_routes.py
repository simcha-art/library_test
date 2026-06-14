# Method	Endpoint	תיאור
# POST	/members	יצירת חבר
# GET	/members	כל החברים
# GET	/members/{id}	חבר לפי ID
# PATCH	/members/{id}	עדכון חבר
# PATCH	/members/{id}/deactivate	השבתת חבר
# PATCH	/members/{id}/activate	הפעלת חבר

from fastapi import APIRouter, HTTPException
from database.member_db import member_manager
from logs.logger_config import logger
import mysql.connector
router = APIRouter()

@router.get("")
def get_all_members():
    logger.info("start getting all members...")
    members = member_manager.get_all_members()
    if not members:
        logger.warning("There are no members to the library!")
    logger.info("complete getting all members")
    return members

@router.get("/{member_id}")
def get_member_by_id(member_id: int):
    logger.info("start getting member by id...")
    member = member_manager.get_member_by_id(member_id)
    if not member:
        logger.warning(f"member {member_id} not found")
        raise HTTPException(404, detail=f"member {member_id} not found")
    
    logger.info(f"member {member_id} found")
    return member


@router.post("", status_code=201)
def create_new_member(data: dict):
    try:
        logger.info("start creating a new member...")
        VALID_FEILDS = {"name", "email"}
        feilds = set(data.keys())
        if feilds != VALID_FEILDS:
            logger.warning(f"invalid feilds, must be of {VALID_FEILDS}")
            raise HTTPException(422, detail=f"invalid feilds, must be {VALID_FEILDS}")
        
        new_id = member_manager.create_member(data)
        if not new_id:
            raise HTTPException(500, detail="internal server error")
        
        return f"member {new_id} created successfully"

    except mysql.connector.Error as e:
        logger.warning("invalid email, it belongs to a different member")
        raise HTTPException(422, detail="invalid email, it belongs to a different member")


    except HTTPException as e:
        logger.error("create member failed")
        raise

    

    
@router.put("{member_id}")
def update_member(member_id: int, data: dict):
    try:
        logger.info(f"start updating member {member_id}...")
        member = member_manager.get_member_by_id(member_id)
        if not member:
            logger.warning(f"member {member_id} not found")
            raise HTTPException(404, detail=f"member {member_id} not found")
        
        VALID_FEILDS = ("name", "email", "is_active", "total_borrows")
        for feild in data.keys():
            if feild not in VALID_FEILDS:
                logger.warning(f"invalid feilds, only {VALID_FEILDS} are valid")
                raise HTTPException(422, f"invalid feilds, only {VALID_FEILDS} are valid")

        success = member_manager.update_member(member_id, data)
        if not success:
            raise HTTPException(400, "already up to date")
        
        return f"update member {member_id} completed"
    
    except mysql.connector.Error:
        logger.warning("duplicated email")
        raise HTTPException(422, "invalid email, belongs to different member")

    except HTTPException as e:
        logger.error("update failed")
        raise


@router.put("/{member_id}/deactivate")
def deactivate_member(member_id: int):
    try:
        member = member_manager.get_member_by_id(member_id)
        if not member:
            logger.warning(f"member {member_id} not found")
            raise HTTPException(404, f"member {member_id} not found")
        
        success = member_manager.deactive_member(member_id)
        if not success:
            logger.warning(f"member {member_id} is already deactive")
            raise HTTPException(400, f"member {member_id} is already deactive")
        
        return f"member {member_id} deactivated successfully"
    
    except HTTPException as e:
        logger.error("deactivate failed")
        raise

@router.put("/{member_id}/activate")
def activate_member(member_id: int):
    try:
        member = member_manager.get_member_by_id(member_id)
        if not member:
            logger.warning(f"member {member_id} not found")
            raise HTTPException(404, f"member {member_id} not found")
        
        success = member_manager.activate_member(member_id)
        if not success:
            logger.warning(f"member {member_id} is already active")
            raise HTTPException(400, f"member {member_id} is already active")
        
        return f"member {member_id} activated successfully"
    except HTTPException as e:
        logger.error("activation failed")
        raise