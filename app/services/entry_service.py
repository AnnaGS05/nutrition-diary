from app.database import get_connection
from app.logger import logger


def get_entries(user_id: int, entry_date: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, proteins, fats, carbs, calories, entry_date, created_at
        FROM entries
        WHERE user_id = %s AND entry_date = %s
        ORDER BY id DESC
    """, (user_id, entry_date))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "proteins": row[2],
            "fats": row[3],
            "carbs": row[4],
            "calories": row[5],
            "entry_date": str(row[6]),
            "created_at": str(row[7])
        }
        for row in rows
    ]


def add_entry(user_id: int, entry):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entries (
            user_id, name, proteins, fats, carbs, calories, entry_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id, name, proteins, fats, carbs, calories, entry_date, created_at
    """, (
        user_id,
        entry.get("name"),
        entry.get("proteins", 0),
        entry.get("fats", 0),
        entry.get("carbs", 0),
        entry.get("calories", 0),
        entry.get("entry_date")
    ))

    row = cursor.fetchone()

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
        "id": row[0],
        "name": row[1],
        "proteins": row[2],
        "fats": row[3],
        "carbs": row[4],
        "calories": row[5],
        "entry_date": str(row[6]),
        "created_at": str(row[7])
    }


def delete_entry(user_id: int, entry_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM entries
        WHERE id = %s AND user_id = %s
    """, (entry_id, user_id))

    deleted = cursor.rowcount > 0

    conn.commit()
    cursor.close()
    conn.close()

    return deleted


def get_stats(user_id: int, entry_date: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COALESCE(SUM(proteins), 0),
            COALESCE(SUM(fats), 0),
            COALESCE(SUM(carbs), 0),
            COALESCE(SUM(calories), 0)
        FROM entries
        WHERE user_id = %s AND entry_date = %s
    """, (user_id, entry_date))

    consumed = cursor.fetchone()

    cursor.execute("""
        SELECT 
            proteins_norm,
            fats_norm,
            carbs_norm,
            calories_norm
        FROM user_profiles
        WHERE user_id = %s
    """, (user_id,))

    norm = cursor.fetchone()

    cursor.close()
    conn.close()

    proteins = consumed[0]
    fats = consumed[1]
    carbs = consumed[2]
    calories = consumed[3]

    if norm:
        proteins_norm = norm[0]
        fats_norm = norm[1]
        carbs_norm = norm[2]
        calories_norm = norm[3]
    else:
        proteins_norm = 0
        fats_norm = 0
        carbs_norm = 0
        calories_norm = 0

    return {
        "proteins": proteins,
        "fats": fats,
        "carbs": carbs,
        "calories": calories,
        "proteins_norm": proteins_norm,
        "fats_norm": fats_norm,
        "carbs_norm": carbs_norm,
        "calories_norm": calories_norm,
        "proteins_percent": round((proteins / proteins_norm * 100), 1) if proteins_norm else 0,
        "fats_percent": round((fats / fats_norm * 100), 1) if fats_norm else 0,
        "carbs_percent": round((carbs / carbs_norm * 100), 1) if carbs_norm else 0,
        "calories_percent": round((calories / calories_norm * 100), 1) if calories_norm else 0
    }