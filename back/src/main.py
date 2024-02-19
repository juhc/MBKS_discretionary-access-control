from fastapi import FastAPI
import asyncio
app = FastAPI(debug=True)

@app.get('/')
async def root():
    await asyncio.sleep(10)
    print('test!!!!')
    return {'message':"MBKS check 1.0"}
