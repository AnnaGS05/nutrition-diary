from app.database import get_connection
from app.logger import logger


def get_entries(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, proteins, fats, carbs, calories, created_at
        FROM entries
        WHERE user_id = %s
        ORDER BY id DESC
    """, (user_id,))

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
            "calories": row[5],
            "created_at": str(row[6])
        }
        for row in rows
    ]


def add_entry(user_id: int, entry):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entries (user_id, name, proteins, fats, carbs, calories)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, name, proteins, fats, carbs, calories, created_at
    """, (
        user_id,
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
        "calories": new_entry[5],
        "created_at": str(new_entry[6])
    }


def delete_entry(user_id: int, entry_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM entries
        WHERE id = %s AND user_id = %s
    """, (entry_id, user_id))

    deleted_count = cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()

    logger.info(
        "entry_deleted",
        extra={
            "path": "/api/entries",
            "status_code": 200
        }
    )

    return deleted_count > 0


def get_stats(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COALESCE(SUM(proteins), 0),
            COALESCE(SUM(fats), 0),
            COALESCE(SUM(carbs), 0),
            COALESCE(SUM(calories), 0)
        FROM entries
        WHERE user_id = %s
    """, (user_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "proteins": row[0],
        "fats": row[1],
        "carbs": row[2],
        "calories": row[3]
    }