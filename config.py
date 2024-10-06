from datetime import timedelta

class Config:
    SECRET_KEY = "YOU_WILL_NEVER_GUESS"
    MONGO_URI = "..."
    PERMANENT_SESSION_LIFETIME = timedelta(weeks=5)
