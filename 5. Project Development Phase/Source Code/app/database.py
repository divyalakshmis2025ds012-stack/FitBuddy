"""
database.py
Handles SQLAlchemy models + all DB read/write helper functions used by routes.py.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)
    schedule = Column(Integer, default=7)  # default 7-day schedule


class WorkoutPlan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_plan = Column(String, nullable=True)
    updated_plan = Column(String, nullable=True)


def init_db():
    """Create tables if they don't exist yet. Called once on app startup."""
    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# User & Plan storage helpers
# ---------------------------------------------------------------------------

def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    existing = db.query(User).filter_by(id=user_id).first()
    if existing:
        existing.name = name
        existing.age = age
        existing.weight = weight
        existing.goal = goal
        existing.intensity = intensity
    else:
        user = User(
            id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            schedule=7,
        )
        db.add(user)
    db.commit()
    db.close()


def save_plan(user_id: int, plan: str):
    """Stores a freshly generated plan as the 'original_plan' for this user."""
    db = SessionLocal()
    workout = WorkoutPlan(user_id=user_id, original_plan=plan)
    db.add(workout)
    db.commit()
    db.close()


def update_plan(user_id: int, updated_text: str):
    """Writes the feedback-revised plan into the most recent WorkoutPlan row."""
    db = SessionLocal()
    workout = (
        db.query(WorkoutPlan)
        .filter_by(user_id=user_id)
        .order_by(WorkoutPlan.id.desc())
        .first()
    )
    if workout:
        workout.updated_plan = updated_text
        db.commit()
    db.close()


def get_original_plan(user_id: int):
    db = SessionLocal()
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user_id)
        .order_by(WorkoutPlan.id.desc())
        .first()
    )
    db.close()
    return plan.original_plan if plan else None


def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user


def get_all_users_with_plans():
    """Used by /view-all-users to build the admin dashboard table."""
    db = SessionLocal()
    users = db.query(User).all()
    user_data = []
    for user in users:
        plan = (
            db.query(WorkoutPlan)
            .filter(WorkoutPlan.user_id == user.id)
            .order_by(WorkoutPlan.id.desc())
            .first()
        )
        user_data.append(
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": plan.original_plan if plan else "N/A",
                "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated",
            }
        )
    db.close()
    return user_data
