import pymongo


class mongo_connect:

    def __init__(self):
    
        # Connect to MongoDB
        # 
        Connection_string = "mongodb+srv://torgunnar1997:YdOKibc2YpOrZI6C@cluster0.w82ra9n.mongodb.net/"
        client = pymongo.MongoClient(Connection_string)
        db = client["mydatabase"]
        self.collection = db["restaurants"]


    def upload(self, data):
        # Example: Insert a document
        
        self.collection.insert_one(data)

    def get_data(self, query):
        # Example: Query documents
        results = self.collection.find(query)
        for doc in results:
            print(doc)

if __name__ == "__main__":
    data = {"name": "Pizza Palace", "cuisine": "Italian"}
    query = {"cuisine": "Italian"}
    
    connect = mongo_connect()
    connect.upload(data = data)
    connect.get_data(query = query)
