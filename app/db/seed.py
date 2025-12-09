# db/seed.py
from sqlmodel import Session, select
from db.database import engine
from models.user import User
from enums.user_role import UserRole
from core.security import hash_password
from core.config import settings


def seed_data():
    """Seed initial data for development"""
    print(f"Seeding database in {settings.environment} environment...")

    with Session(engine) as session:
        try:
            # Check if users already exist
            existing_users = session.exec(select(User)).all()
            if existing_users:
                print("Users already exist, skipping seeding...")
                return

            # Create one user for each role
            users = [
                User(
                    first_name="John",
                    last_name="CEO",
                    email="ceo@example.com",
                    hashed_password=hash_password("password123"),
                    user_role=UserRole.CEO,
                ),
                User(
                    first_name="Sarah",
                    last_name="Pharma",
                    email="pharma.manager@example.com",
                    hashed_password=hash_password("password123"),
                    user_role=UserRole.PHARMA_MANAGER,
                ),
                User(
                    first_name="Mike",
                    last_name="Procurement",
                    email="procurement.manager@example.com",
                    hashed_password=hash_password("password123"),
                    user_role=UserRole.PROCUREMENT_MANAGER,
                ),
                User(
                    first_name="Lisa",
                    last_name="Technical",
                    email="technical.manager@example.com",
                    hashed_password=hash_password("password123"),
                    user_role=UserRole.TECHNICAL_MANAGER,
                ),
                User(
                    first_name="David",
                    last_name="Site",
                    email="site.manager@example.com",
                    hashed_password=hash_password("password123"),
                    user_role=UserRole.SITE_MANAGER,
                ),
                User(
                    first_name="Emma",
                    last_name="SitePharma",
                    email="site.pharma@example.com",
                    hashed_password=hash_password("password123"),
                    user_role=UserRole.SITE_PHARMA_MANAGER,
                ),
                User(
                    first_name="Tom",
                    last_name="Fridge",
                    email="fridge.manager@example.com",
                    hashed_password=hash_password("password123"),
                    user_role=UserRole.TECHNICAL_FRIDGE_MANAGER,
                ),
            ]

            session.add_all(users)
            session.commit()

            print(f"✓ Created {len(users)} users (one per role)")
            print("\nSeeded users:")
            for user in users:
                print(
                    f"  - {user.email} ({user.user_role.name}) - password: password123"
                )

            print("\n✓ Database seeding completed")

        except Exception as e:
            print(f"Error seeding database: {e}")
            session.rollback()
            raise


if __name__ == "__main__":
    seed_data()
