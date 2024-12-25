from fastapi import FastAPI,APIRouter
from database.config import collection
from database.config import shop_collection
from models.laptop import Laptop
from models.laptop import desearialize,desearialize_list
from typing import Optional
from pydantic import Field
from bson import ObjectId



laptop_route = APIRouter()

@laptop_route.get('/lap/laptops')
async def get_laptops():
    try:
        data = collection.find({})

        if data:
            return {"laptops": desearialize_list(data)}
        else:
            return {"message": "No laptops found"}
    except Exception:
        return {"message": "Error fetching laptops"}


@laptop_route.post("/lap/add")
async def add_laptop(laptop:Laptop):
    try:
        collection.insert_one(dict(laptop))
        return {"message":"laptop added"}
    except Exception as e :
        return {"message":e}

@laptop_route.delete("/lap/delete")
async def delete_laptop(name:str):
    try:
        collection.delete_one({"name":name})
        return {"message":"laptop deleted"} 
    except Exception as e :
        return {"message":"error"}


@laptop_route.get("/lap/info")
async def get_info(name:Optional[str] = "",os:Optional[str] = "",displayres:Optional[str] = "",primary_use:Optional[str] = "",battery:Optional[int] = 0,ram:Optional[int] = 0,storage:Optional[str] = "",displaysize:Optional[int] = 0,weight:Optional[float] = 0.0,Rating:Optional[float] = 0.0,Processor:Optional[str] = "",budget:Optional[int] = 0):  

    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if os:
        query["os"] = os
    if displayres:
        query["displayres"] = displayres
    if primary_use:
        query["primary_use"] = primary_use
    if battery:
        query["battery"] = {"$gte": battery}
    if ram:
        query["ram"] = {"$gte": ram}
    if storage:
        query["storage"] = storage
    if displaysize:
        query["displaysize"] = {"$gte": displaysize}
    if weight:
        query["weight"] = {"$lte": weight}
    if Rating:
        query["Rating"] = {"$gte": Rating},
    if Processor:
        query["Processor"] = {"$regex": Processor, "$options": "i"}
    if budget:
        query["budget"] = {"$lte": budget}
    # query = {
    #     "name": {"$regex": name, "$options": "i"},
    #     "ram": {"$gt": ram},
    #     "storage": {"$gt": storage},
    #     "battery": {"$gt": battery},
    #     "Rating": {"$gt": Rating},
    #     "weight": {"$lt": weight},
    #     "displaysize": {"$gt": displaysize}
    # }

    print(query)
    data = collection.find(query)
    return {"message":desearialize_list(data)}


@laptop_route.put("/lap/update_rating")
async def update_laptop_rating(user:str,name:str,new_rating:float):
    old_rating = collection.find_one({"user":user,"name":name})
    if old_rating:
        print("found user")
        d = desearialize(old_rating) 
        x = (d["Rating"] + new_rating) / 2
        collection.update_one({"user":user,"name":name}, {"$set":{"Rating":x}})
        shop_collection.update_one({"_id": ObjectId(user), "laptops.name": name}, {"$set": {"laptops.$.Rating": x}})
        return {"message":"rating updated successfully"}
    else:
        {"message":"user or laptop not found"}
    
 