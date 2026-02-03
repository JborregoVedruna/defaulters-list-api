"""insert_data_debts_table

Revision ID: a6e710cb959c
Revises: 25ea8732b426
Create Date: 2026-01-28 23:35:51.096892

"""
from typing import Sequence, Union

import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# revision identifiers, used by Alembic.
revision: str = 'a6e710cb959c'
down_revision: Union[str, Sequence[str], None] = '25ea8732b426'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Reusable data for upgrade and downgrade
DATA_TO_INSERT = [
    {
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "debtor_name": "alejandro_garcia",
        "debtor_dni": "12345678Z",
        "debt_amount": 300.0,
        "currency": "EUR",
        "debt_since": datetime.fromisoformat("2026-01-28T23:37:36")
    },
    {
        "uuid": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
        "debtor_name": "lucia_fernandez",
        "debtor_dni": "23456789D",
        "debt_amount": 150.0,
        "currency": "GBP",
        "debt_since": datetime.fromisoformat("2026-01-01T23:37:36")
    }
]

def upgrade() -> None:
    """Upgrade schema."""
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME")

    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")

    client = MongoClient(mongo_uri)
    db = client[mongo_db_name]

    db["debts"].insert_many(DATA_TO_INSERT)
    client.close()


def downgrade() -> None:
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME")

    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")

    client = MongoClient(mongo_uri)
    db = client[mongo_db_name]

    # Remove by UUID
    uuids = [d["uuid"] for d in DATA_TO_INSERT]
    db["debts"].delete_many({"uuid": {"$in": uuids}})

    client.close()
