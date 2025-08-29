from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session

from app.db import get_session
from app.auth import get_current_user
from app.models import JobApplication, JobApplicationCreate, JobApplicationRead, StatusEnum

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=JobApplicationRead, status_code=201)
def add_application(
    payload: JobApplicationCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user),
):
    # Build entity with current user
    app = JobApplication(**payload.model_dump(), user_id=user_id)
    session.add(app)
    session.commit()
    session.refresh(app)
    return app

@router.get("/", response_model=List[JobApplicationRead])
def list_applications(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=500, description="Max number of items"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    stmt = (
        select(JobApplication)
        .where(JobApplication.user_id == user_id)
        .order_by(JobApplication.id.desc())
        .limit(limit)
        .offset(offset)
    )
    results = session.exec(stmt).all()
    return results

@router.get("/search", response_model=List[JobApplicationRead])
def search_applications(
    status: StatusEnum = Query(..., description="Filter by status"),
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user),
):
    # Additional guardrail, though pydantic/enum already validates
    if status not in StatusEnum.__members__.values():
        raise HTTPException(status_code=400, detail="Invalid status")
    stmt = select(JobApplication).where(
        (JobApplication.user_id == user_id) & (JobApplication.status == status)
    ).order_by(JobApplication.id.desc())
    return session.exec(stmt).all()
