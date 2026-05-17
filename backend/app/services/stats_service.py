from datetime import date, timedelta

from app.database import get_connection


def get_weekly_stats(user_id: int) -> dict:
    today = date.today()
    start_date = today - timedelta(days=6)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            entry_date,
            COALESCE(SUM(proteins), 0),
            COALESCE(SUM(fats), 0),
            COALESCE(SUM(carbs), 0),
            COALESCE(SUM(calories), 0)
        FROM entries
        WHERE user_id = %s
          AND entry_date BETWEEN %s AND %s
        GROUP BY entry_date
        ORDER BY entry_date
    """, (user_id, start_date, today))

    rows = cursor.fetchall()

    cursor.execute("""
        SELECT proteins_norm, fats_norm, carbs_norm, calories_norm
        FROM user_profiles
        WHERE user_id = %s
    """, (user_id,))

    norm_row = cursor.fetchone()

    cursor.close()
    conn.close()

    data_by_date = {
        str(row[0]): {
            "proteins": float(row[1]),
            "fats":     float(row[2]),
            "carbs":    float(row[3]),
            "calories": float(row[4])
        }
        for row in rows
    }

    days = []
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        key = str(current_date)
        values = data_by_date.get(key, {"proteins": 0, "fats": 0, "carbs": 0, "calories": 0})
        days.append({"date": key, "label": current_date.strftime("%d.%m"), **values})

    avg_proteins = round(sum(d["proteins"] for d in days) / 7, 1)
    avg_fats     = round(sum(d["fats"]     for d in days) / 7, 1)
    avg_carbs    = round(sum(d["carbs"]    for d in days) / 7, 1)
    avg_calories = round(sum(d["calories"] for d in days) / 7, 1)

    best_day = max(days, key=lambda d: d["calories"])

    if norm_row:
        norm = {
            "proteins": float(norm_row[0]),
            "fats":     float(norm_row[1]),
            "carbs":    float(norm_row[2]),
            "calories": float(norm_row[3])
        }
    else:
        norm = {"proteins": 0, "fats": 0, "carbs": 0, "calories": 0}

    return {
        "days": days,
        "average": {"proteins": avg_proteins, "fats": avg_fats, "carbs": avg_carbs, "calories": avg_calories},
        "norm": norm,
        "best_day": best_day
    }
