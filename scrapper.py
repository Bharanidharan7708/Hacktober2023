from pymilvus import connections
from pymilvus import utility
from pymilvus import Collection


connections.connect(          #yo connect with db
    host='20.244.48.175',
    port='19530'
)

utility.list_collections() #use this line to display the collections inside the db, our collection name is ITC_ITCHOTELS_scrapped

collection = Collection("ITC_ITCHOTELS_scrapped")

collection.schema #to get the schema

query_result = collection.query(output_fields=["id", "text"], limit=20, expr="")

for result in query_result:
    print(result)
