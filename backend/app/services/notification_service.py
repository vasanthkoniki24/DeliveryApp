from sqlalchemy.orm import Session
from app.models.notification import Notification


def create_notification(db: Session, user_id: int, message: str):
    notif = Notification(
        user_id=user_id,
        message=message
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def get_notifications(db: Session, user_id: int):
    return db.query(Notification)\
        .filter(Notification.user_id == user_id)\
        .order_by(Notification.created_at.desc())\
        .all()