from app.database import get_connection


def calculate_norms(age, height, weight, gender, activity, goal):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    calories = bmr * activity

    if goal == "loss":
        calories -= 300
    elif goal == "gain":
        calories += 300

    proteins = weight * 1.6
    fats = weight * 0.9
    carbs = (calories - proteins * 4 - fats * 9) / 4

    return {
        "calories_norm": round(calories, 2),
        "proteins_norm": round(proteins, 2),
        "fats_norm": round(fats, 2),
        "carbs_norm": round(carbs, 2)
    }


def save_profile(user_id, profile):
    age = int(profile["age"])
    height = float(profile["height"])
    weight = float(profile["weight"])
    gender = profile["gender"]
    activity = float(profile["activity"])
    goal = profile["goal"]

    norms = calculate_norms(age, height, weight, gender, activity, goal)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_profiles (
            user_id, age, height, weight, gender, activity, goal,
            calories_norm, proteins_norm, fats_norm, carbs_norm
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET
            age = EXCLUDED.age,
            height = EXCLUDED.height,
            weight = EXCLUDED.weight,
            gender = EXCLUDED.gender,
            activity = EXCLUDED.activity,
            goal = EXCLUDED.goal,
            calories_norm = EXCLUDED.calories_norm,
            proteins_norm = EXCLUDED.proteins_norm,
            fats_norm = EXCLUDED.fats_norm,
            carbs_norm = EXCLUDED.carbs_norm
    """, (
        user_id, age, height, weight, gender, activity, goal,
        norms["calories_norm"],
        norms["proteins_norm"],
        norms["fats_norm"],
        norms["carbs_norm"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return norms


def get_profile(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT age, height, weight, gender, activity, goal,
               calories_norm, proteins_norm, fats_norm, carbs_norm
        FROM user_profiles
        WHERE user_id = %s
    """, (user_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "age": row[0],
        "height": row[1],
        "weight": row[2],
        "gender": row[3],
        "activity": row[4],
        "goal": row[5],
        "calories_norm": row[6],
        "proteins_norm": row[7],
        "fats_norm": row[8],
        "carbs_norm": row[9]
    }