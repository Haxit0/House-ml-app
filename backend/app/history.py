from .db import get_connection


def load_prediction_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            area_sqft,
            bedrooms,
            bathrooms,
            location_score,
            age_years,
            predicted_price,
            actual_price
        FROM feedback
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        (
            record_id,
            area_sqft,
            bedrooms,
            bathrooms,
            location_score,
            age_years,
            predicted_price,
            actual_price,
        ) = row

        error = None
        if predicted_price is not None and actual_price is not None:
            error = actual_price - predicted_price

        history.append(
            {
                "id": record_id,
                "area_sqft": area_sqft,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "location_score": location_score,
                "age_years": age_years,
                "predicted_price": predicted_price,
                "actual_price": actual_price,
                "error": error,
            }
        )

    return history