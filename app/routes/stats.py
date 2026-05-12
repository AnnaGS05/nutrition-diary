from datetime import date, timedelta

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from app.database import get_connection
from app.services.auth_service import get_current_user_id

router = APIRouter(prefix="/api/stats", tags=["Stats"])


@router.get("/weekly")
def weekly_stats(request: Request):
    user_id = get_current_user_id(request)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

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

    data_by_date = {
        str(row[0]): {
            "proteins": float(row[1]),
            "fats": float(row[2]),
            "carbs": float(row[3]),
            "calories": float(row[4])
        }
        for row in rows
    }

    days = []

    for i in range(7):
        current_date = start_date + timedelta(days=i)
        key = str(current_date)

        values = data_by_date.get(key, {
            "proteins": 0,
            "fats": 0,
            "carbs": 0,
            "calories": 0
        })

        days.append({
            "date": key,
            "label": current_date.strftime("%d.%m"),
            **values
        })

    avg_proteins = round(sum(day["proteins"] for day in days) / 7, 1)
    avg_fats = round(sum(day["fats"] for day in days) / 7, 1)
    avg_carbs = round(sum(day["carbs"] for day in days) / 7, 1)
    avg_calories = round(sum(day["calories"] for day in days) / 7, 1)

    best_day = max(days, key=lambda item: item["calories"])

    if norm:
        proteins_norm = float(norm[0])
        fats_norm = float(norm[1])
        carbs_norm = float(norm[2])
        calories_norm = float(norm[3])
    else:
        proteins_norm = 0
        fats_norm = 0
        carbs_norm = 0
        calories_norm = 0

    return JSONResponse(
        content={
            "days": days,
            "average": {
                "proteins": avg_proteins,
                "fats": avg_fats,
                "carbs": avg_carbs,
                "calories": avg_calories
            },
            "norm": {
                "proteins": proteins_norm,
                "fats": fats_norm,
                "carbs": carbs_norm,
                "calories": calories_norm
            },
            "best_day": best_day
        },
        media_type="application/json; charset=utf-8"
    )