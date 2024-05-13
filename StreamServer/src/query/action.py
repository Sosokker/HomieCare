from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models import ActionData


def get_weekly_action_data(session: Session):
    """
    Get the list of actions for the this week.
    """
    date_7_days_ago = (datetime.now() - timedelta(days=7)).date()

    return session.query(ActionData).filter(
        func.date(ActionData.timestamp) >= date_7_days_ago
    ).all()