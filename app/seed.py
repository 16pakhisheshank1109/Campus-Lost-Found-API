"""Insert a repeatable set of sample lost-and-found reports."""

from sqlmodel import Session, select

from .database import create_db_and_table, engine
from .models import Item

SAMPLE_ITEMS = [
    {
        "title": "Blue water bottle",
        "description": "Insulated bottle left in the library study area.",
        "category": "Bottle",
        "location": "Main Library",
        "reported_by": "Aarav Sharma",
        "status": "Lost",
    },
    {
        "title": "Student ID card",
        "description": "University ID card found near the north entrance.",
        "category": "ID Card",
        "location": "Science Building",
        "reported_by": "Maya Patel",
        "status": "Found",
    },
    {
        "title": "Black umbrella",
        "description": "Compact umbrella found after the afternoon lecture.",
        "category": "Accessories",
        "location": "Lecture Hall B",
        "reported_by": "Noah Williams",
        "status": "Found",
    },
    {
        "title": "Notebook returned",
        "description": "Red notebook returned to its owner at the help desk.",
        "category": "Stationery",
        "location": "Student Center",
        "reported_by": "Isha Gupta",
        "status": "Returned",
    },
]


def seed_database() -> int:
    """Add sample records that are not already present by title."""
    create_db_and_table()
    added = 0
    with Session(engine) as session:
        for sample in SAMPLE_ITEMS:
            existing = session.exec(
                select(Item).where(Item.title == sample["title"])
            ).first()
            if existing is None:
                session.add(Item(**sample))
                added += 1
        session.commit()
    return added


if __name__ == "__main__":
    print(f"Added {seed_database()} sample item(s).")
