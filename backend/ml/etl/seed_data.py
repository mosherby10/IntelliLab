import random
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import User, Submission


def seed():
    db = SessionLocal()

    for i in range(10):
        email = f"user{i}@example.com"
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                full_name=f"User {i}",
                email=email,
                hashed_password="fakehashedpassword",
                is_instructor=False
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Add submissions (only if the user doesn’t already have them)
        existing_subs = db.query(Submission).filter(Submission.user_id == user.id).count()
        if existing_subs < 5:
            for j in range(5 - existing_subs):
                sub = Submission(
                    user_id=user.id,
                    course=f"Course {random.randint(1, 3)}",
                    content=f"This is a fake submission {j} from {user.full_name}",
                    score=random.uniform(30, 100),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                db.add(sub)

    db.commit()
    db.close()
    print("✅ Seeding completed (safe, no duplicates).")


if __name__ == "__main__":
    seed()
