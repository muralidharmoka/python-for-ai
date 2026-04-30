
from fastapi import FastAPI, HTTPException
from datetime import date, timedelta

app = FastAPI()

#FAKE DATA FOR TESTING PURPOSES
fake_orders = {
    1:{
        "user_id": 1,
        "item": "Laptop",
        "quantity": 1,
        "delevery_date": date.today() + timedelta(days=2),
        "status": "Out for Delivery"
    },
    2:{
        "user_id": 2,
        "item": "Headphones",
        "quantity": 2,
        "delevery_date": date.today() + timedelta(days=5),
        "status": "Shipped  "
    },
    3:{
        "user_id": 3,
        "item": "Book",
        "quantity": 1,
        "delevery_date": date.today() + timedelta(days=1),  
        "status": "Arriving tomorrow"
    }

}

#API END POINT

@app.get("/delivery_status/{user_id}")
def get_delivery(user_id: int):
    if user_id not in fake_orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return fake_orders[user_id]
