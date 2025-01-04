from os import getenv
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient


class Database:
      # Load environment variables and connect to the database
    

    def __init__(self, collection_name: str):
        """
        Initialize the Database instance with a specific collection.
        :param collection_name: The name of the MongoDB collection to interact with.
        """
        load_dotenv()
        self.database = MongoClient(getenv("DB_URL"), tlsCAFile=where())["BanderSnatch"]
        self.collection = self.database.get_collection(collection_name)

    def seed(self, amount: int):
        """
        Insert the specified number of random monster documents into the collection.
        :param amount: Number of documents to insert.
        """
        monsters = [Monster().to_dict() for _ in range(amount)]
        self.collection.insert_many(monsters)

    def reset(self):
        """
        Delete all documents from the collection.
        """
        self.collection.delete_many({})

    def count(self) -> int:
        """
        Return the total number of documents in the collection.
        :return: Document count.
        """
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        """
        Return the collection data as a Pandas DataFrame.
        :return: DataFrame containing all documents in the collection.
        """
        data = list(self.collection.find({}, {"_id": False}))
        return DataFrame(data)

    def html_table(self) -> str:
        """
        Return an HTML table representation of the collection's data.
        :return: HTML table as a string, or None if the collection is empty.
        """
        df = self.dataframe()
        return df.to_html(index=False) if not df.empty else None

# Testing Script
if __name__ == "__main__":
    # Initialize the Database with the "Monster" collection
    db = Database("Monster")

    # Reset the database
    db.reset()
    print("Database reset.")

    # Seed the database with 20 monsters
    db.seed(20)
    print("Database seeded with 20 monsters.")

    # Print the number of documents in the collection
    print(f"Document count: {db.count()}")

    # Display the collection as a DataFrame
    print("DataFrame:")
    print(db.dataframe())

    # Generate and display an HTML table of the collection
    print("HTML Table:")
    html = db.html_table()
    print(html if html else "No data in the collection.")