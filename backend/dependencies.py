
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models_orm

def get_current_user(x_user_email: str = Header(None), db: Session = Depends(get_db)):
    """
    Simulates authentication by trusting the X-User-Email header from the Next.js frontend.
    For MVP only.
    """
    if not x_user_email:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # simplistic: get or create user
    user = db.query(models_orm.User).filter(models_orm.User.email == x_user_email).first()
    if not user:
        # Auto-create for now if not found (or raise 401 if strict)
        user = models_orm.User(email=x_user_email, full_name="Researcher") # Default name
        db.add(user)
        db.commit()
        db.refresh(user)
        
    return user
