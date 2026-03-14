import asyncio
from sqlalchemy import text
from app.db.session import async_session_factory, engine

async def check():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("ALTER TABLE participants ADD COLUMN IF NOT EXISTS user_id INTEGER;"))
            try:
                await conn.execute(text("ALTER TABLE participants ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(user_id);"))
                print("Constraint added.")
            except Exception as e:
                print("Constraint might already exist:", e)
            result = await conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'participants';"))
            cols = [row[0] for row in result]
            print("Participants columns:", cols)
    except Exception as e:
        print("Error:", e)

asyncio.run(check())
