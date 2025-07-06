ALLOWED_PREFERENCES = {
    "news_preferences": ["notification_time", "user_id"],
    "sport_preference" : ["sport_team"]
}




# data = {  "news_preferences": ["notification_time", "user_id"]}

# selected_data = data['news_preference']
# print(selected_data)

# @app.post("/add-preference")
# def add_preference(
#     payload: dict = Depends(verify_token),
#     preference: GenericPreference = Depends()
# ):
#     if payload is None:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     user_id = payload.get("user_id")
#     if not user_id:
#         raise HTTPException(status_code=400, detail="Invalid token payload")

#     table = preference.table
#     data = preference.data

#     # Validate table and fields
#     if table not in ALLOWED_PREFERENCES:
#         raise HTTPException(status_code=400, detail="Invalid table")

#     allowed_fields = ALLOWED_PREFERENCES[table]
#     for field in data.keys():
#         if field not in allowed_fields:
#             raise HTTPException(status_code=400, detail=f"Invalid field: {field}")

#     # Add user_id automatically if not present
#     if "user_id" in allowed_fields and "user_id" not in data:
#         data["user_id"] = user_id

#     columns = ", ".join(data.keys())
#     placeholders = ", ".join(["%s"] * len(data))
#     values = tuple(data.values())

#     query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

#     # DB insert
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute(query, values)
#         connection.commit()
#         return {"message": "Preference saved"}
#     except Exception as e:
#         connection.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close()
#         connection.close()
