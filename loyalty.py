import time
import schedule
import traceback
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId to convert string IDs

def get_database():
    """
    Connects to MongoDB Atlas using the provided connection string,
    pings the server to verify the connection, and returns the 'oms_db' database.
    """
    CONNECTION_STRING = ("Your connection string")
    
    client = MongoClient(CONNECTION_STRING)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. Successfully connected to MongoDB!")
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        exit(1)
    
    return client['oms_db']

# Get the database
db = get_database()
print("Connected to the database successfully!")

# Define the collections
orders_collection = db['orders']
users_collection = db['users']

def update_loyalty_points():
    """
    Fetches orders with a status of 'Shipped', tallies the count of such orders per customer,
    and updates each customer's loyalty points in the users collection.
    """
    try:
        shipped_orders = orders_collection.find({"status": "Shipped"})
        
        loyalty_counts = {}
        for order in shipped_orders:
            customer_id_str = order.get('customer_id')
            if not customer_id_str:
                print("Order missing customer_id field:", order)
                continue
            
            # Convert the string to an ObjectId because thats the type on mongo
            try:
                customer_id = ObjectId(customer_id_str)
            except Exception as e:
                print(f"Error converting customer_id {customer_id_str} to ObjectId:", e)
                continue
            
            loyalty_counts[customer_id] = loyalty_counts.get(customer_id, 0) + 1

        for customer_id, points in loyalty_counts.items():
            result = users_collection.update_one(
                {"_id": customer_id},
                {"$set": {"loyalty_points": points}}
            )
            print(f"Updated user with _id {customer_id}: loyalty_points set to {points} "
                  f"(Matched: {result.matched_count}, Modified: {result.modified_count})")

        print("Loyalty points update complete at", time.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print("Error updating loyalty points:")
        traceback.print_exc()

# Schedule the job to run every two hours
schedule.every(2).hours.do(update_loyalty_points)

# Run 
update_loyalty_points()

while True:
    schedule.run_pending()
    time.sleep(1)
