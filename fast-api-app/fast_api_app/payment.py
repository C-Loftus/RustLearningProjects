import time
from fastapi import FastAPI
from fastapi.middleware import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from fastapi.background import BackgroundTask
import os, requests
from starlette.requests import Request
# Load environment variable
from dotenv import load_dotenv
load_dotenv()



app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="redis-18548.c11.us-east-1-3.ec2.cloud.redislabs.com",
    port=18548,
    password = os.getenv("password"),
    decode_responses=True
)
class Order(HashModel):
    product_id: str
    price: float
    fee: float
    quantity: int
    total: float
    status: str

    class Meta: 
        database=redis


    @app.post("/orders")
    async def create(request: Request, background_task: BackgroundTask):
        body=await request.json()

        req = requests.get("://localhost:3000/products/%s" % body[id])
        product=req.json()
        order = Order(
            product_id=body[id],
            price=product['price'],
            fee= 0.2 * product['price'],
            quantity=body["quantity"],
            total=1.2*product['price'],
            status="pending"
        )
        order.save()
        background_task.add_task(order_completed, order)

        return order
def order_completed(order: Order):
    time.sleep(5)
    order.status="completed"
    order.save()
    redis.xadd("order_completed", order.dict(),  '*')
    return order

@app.get("/orders/{pk}")
def get(pk: str):
    return Order.get(pk)