# Loyalty Microservice

This microservice connects to a MongoDB database, calculates loyalty points based on orders with a `"Shipped"` status, and updates each customer's record in the users collection.

## Overview

- **Function:**  
  The microservice tallies the number of orders with a `"Shipped"` status for each customer and updates the corresponding user's `loyalty_points` field in the MongoDB database.

- **Operation:**  
  The service runs continuously, updating the data every two hours and once immediately upon startup.

- **Communication Contract:**  
  This document describes how to start (i.e., request) and retrieve (i.e., receive) data processed by the microservice.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kotoiw/loyalty-microservice.git
   cd loyalty-microservice
Install Dependencies:
Ensure you have Python 3 installed, then run:

bash
Copy
pip install pymongo[srv] schedule
Configure Your MongoDB Connection:
The connection string is currently hardcoded in the source file (loyalty_microservice.py). Update it if needed.

Running the Microservice
To start the microservice, run:

bash
Copy
python loyalty_microservice.py
When you run the program, it will:

Connect to MongoDB and print a confirmation message if the connection is successful.
Immediately process the orders.
Schedule loyalty points updates every two hours.
Communication Contract
Requesting Data (Starting the Service)
The microservice does not expose an HTTP endpoint. Instead, your teammate can "request" data by simply running the service. The service will start processing as soon as it is executed.

Example Request:
Run the following command in your terminal or include it in your deployment script:
bash
Copy
python loyalty_microservice.py
This command starts the microservice, which will continuously update the database with calculated loyalty points.
Receiving Data (Retrieving the Processed Information)
After the microservice runs, it updates the loyalty_points field in the users collection of your MongoDB database. Your teammate can query the database to retrieve the updated data.

Example Call to Receive Data:
Here’s a sample Python snippet that demonstrates how to retrieve a user’s updated loyalty points:
python
Copy
from pymongo import MongoClient
from bson import ObjectId

# Replace with your actual connection string
CONNECTION_STRING = (This is your connection string for Mongodb)

client = MongoClient(CONNECTION_STRING)

db = client['oms_db']
