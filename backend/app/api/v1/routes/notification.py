from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db, get_current_user
from app.schemas.notification import NotificationResponse
from app.services.notification_service import get_notifications

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=list[NotificationResponse])
def fetch_notifications(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_notifications(db, user.id)