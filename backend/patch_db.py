import asyncio
from sqlalchemy import text
from app.db.session import async_session_factory
from app.db.models import Base
from sqlalchemy import inspect

async def migrate_event_codes():
    async with async_session_factory() as session:
        try:
            print("Beginning migration for event_codes table...")
            
            # Step 1: Add new columns
            await session.execute(text("ALTER TABLE event_codes ADD COLUMN IF NOT EXISTS participant_code VARCHAR(20);"))
            await session.execute(text("ALTER TABLE event_codes ADD COLUMN IF NOT EXISTS organizer_code VARCHAR(20);"))
            print("Added new columns.")

            # Step 2: Migrate existing data
            # Use the old code for participant_code and generate a new one for organizer_code 
            await session.execute(text(
                "UPDATE event_codes SET participant_code = code, organizer_code = CONCAT('MIG-O-', code_id) WHERE participant_code IS NULL;"
            ))
            print("Migrated existing data.")

            # Step 3: Add constraints
            await session.execute(text("ALTER TABLE event_codes ALTER COLUMN participant_code SET NOT NULL;"))
            await session.execute(text("ALTER TABLE event_codes ALTER COLUMN organizer_code SET NOT NULL;"))
            await session.execute(text("ALTER TABLE event_codes ADD CONSTRAINT uq_participant_code UNIQUE (participant_code);"))
            await session.execute(text("ALTER TABLE event_codes ADD CONSTRAINT uq_organizer_code UNIQUE (organizer_code);"))
            print("Added constraints.")

            # Step 4: Drop old column
            await session.execute(text("ALTER TABLE event_codes DROP COLUMN IF EXISTS code;"))
            print("Dropped old code column.")

            await session.commit()
            print("Migration completed successfully.")
        except Exception as e:
            await session.rollback()
            print(f"Error during migration: {e}")

if __name__ == "__main__":
    asyncio.run(migrate_event_codes())
