import asyncio
from httpx import AsyncClient, ASGITransport
from main import app

async def main():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/organizer/events/2/run_emergency",
            json={"problem_description": "We have an emergency!!"}
        )
        print("Status", response.status_code)
        print("Body", response.text)

asyncio.run(main())
