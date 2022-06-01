from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import os 
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
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta: 
        database=redis


@app.get("/products")
def all():
    return [format(pk)for pk in Product.all_keys()]
def format(pk: str):
    product=Product.get(pk)

    return {
        "name": product.name, 
        'id': product.pk,
        "price": product.price,
        "quantity": product.quantity
    }


@app.post("/products")
def create(product: Product):
    return product.save()

@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)

@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)