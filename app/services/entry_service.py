from app.database import get_connection
from app.logger import logger


def get_entries():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, proteins, fats, carbs, calories
        FROM entries
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    logger.info(
        "entries_loaded",
        extra={
            "path": "/api/entries",
            "status_code": 200
        }
    )

    return [
        {
            "id": row[0],
            "name": row[1],
            "proteins": row[2],
            "fats": row[3],
            "carbs": row[4],
            "calories": row[5]
        }
        for row in rows
    ]


def add_entry(entry):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entries (name, proteins, fats, carbs, calories)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, name, proteins, fats, carbs, calories
    """, (
        entry.get("name"),
        entry.get("proteins", 0),
        entry.get("fats", 0),
        entry.get("carbs", 0),
        entry.get("calories", 0)
    ))

    new_entry = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    logger.info(
        "entry_created",
        extra={
            "path": "/api/entries",
            "status_code": 201
        }
    )

    return {
        "id": new_entry[0],
        "name": new_entry[1],
        "proteins": new_entry[2],
        "fats": new_entry[3],
        "carbs": new_entry[4],
        "calories": new_entry[5]
    }