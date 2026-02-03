"""create_debts_collection

Revision ID: 25ea8732b426
Revises: 
Create Date: 2026-01-28 23:13:18.615814

"""
from typing import Sequence, Union
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# revision identifiers, used by Alembic.
revision: str = '25ea8732b426'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """
    This migration script creates a collection named "debts" in the MongoDB database.
    It also creates a validator for the collection to ensure that the data is valid.
    """
    # Connect to MongoDB
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME")

    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")

    client = MongoClient(mongo_uri)

    # Select database
    db = client[mongo_db_name]

    # Drop collection if it exists (Equivalent to DROP TABLE IF EXISTS)
    # Note: validation actions are usually on create, so we recreate for
    # schema updates in this script approach
    if "debts" in db.list_collection_names():
        db["debts"].drop()

    # Create collection with validator (Equivalent to CREATE TABLE with constraints)
    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["uuid", "debtor_name", "debtor_dni", 
            "debt_amount", "currency", "debt_since"],
            "properties": {
                "uuid": {
                    "bsonType": "string",
                    "description": "must be a string (UUID) and is required"
                },
                "debtor_name": {
                    "bsonType": "string",
                    "maxLength": 45,
                    "description": "must be a string (max length 45) and is required"
                },
                "debtor_dni": {
                    "bsonType": "string",
                    "maxLength": 9,
                    "description": "must be a string (max length 9) and is required"
                },
                "debt_amount": {
                    "bsonType": ["decimal", "double"], 
                    "description": "must be a decimal or double and is required"
                },
                "currency": {
                    "bsonType": "string",
                    "maxLength": 3,
                    "description": "must be a string and is required"
                },
                "debt_since": {
                    "bsonType": "date",
                    "description": "must be a date and is required"
                }
            }
        }
    }

    db.create_collection("debts", validator=validator)

    # Create unique index for primary key equivalent
    db["debts"].create_index("uuid", unique=True)

    client.close()


def downgrade() -> None:
    """
    This migration script drops the "debts" collection from the MongoDB database.
    """
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME")

    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")

    client = MongoClient(mongo_uri)
    db = client[mongo_db_name]

    # Drop collection
    if "debts" in db.list_collection_names():
        db["debts"].drop()

    client.close()
