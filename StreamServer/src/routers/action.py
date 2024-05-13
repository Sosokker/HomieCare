from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

from scheme import ActionData
from query.action import get_weekly_action_data
from database import engine, SessionLocal, Base


Base.metadata.create_all(bind=engine)

router = APIRouter()

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


@router.get("/week", response_model=list[ActionData])
async def get_week_action(db: Session = Depends(get_db)):
    """Return the list of ActionData for the this week."""
    action_data = get_weekly_action_data(db)
    if not action_data:
        raise HTTPException(status_code=404, detail="Action data for the last week not found")
    return action_data