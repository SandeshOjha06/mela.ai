import asyncio
from sqlalchemy import select
from app.db.models import SwarmLog, EmergencyLog, Ticket
from app.api.deps import async_session_factory

async def main():
    async with async_session_factory() as db:
        res = await db.execute(select(SwarmLog).where(SwarmLog.event_id == 2).order_by(SwarmLog.created_at.desc()).limit(10))
        for log in res.scalars():
            print("SwarmLog:", log.created_at, log.agent_name, log.action_taken[:100])
        
        # Check tickets
        t_res = await db.execute(select(Ticket).where(Ticket.event_id == 2).order_by(Ticket.created_at.desc()).limit(2))
        for t in t_res.scalars():
            print("Ticket:", t.created_at, t.problem_category, t.status)

        # Check emergency logs
        e_res = await db.execute(select(EmergencyLog).where(EmergencyLog.event_id == 2).order_by(EmergencyLog.created_at.desc()).limit(2))
        for e in e_res.scalars():
            print("EmergencyLog:", e.created_at, e.problem_description)

asyncio.run(main())
