import aiohttp
import asyncio

base_url = "http://localhost:3000"

async def get_message(_type, id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/{_type}/{id}") as responce:
                res = await responce.json()
                return res
    except: 
        print(f"Failed to get message from {base_url}/{_type}/{id}")

async def postInfo(_type, id, data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{base_url}/{_type}/{id}", json=data) as responce:
                res = await responce.json()
                return res
    except:
        print(f"Failed to post to {base_url}/{_type}/{id}")
