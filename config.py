from datetime import timedelta

class Config:
    SECRET_KEY = "YOU_WILL_NEVER_GUESS"
    MONGO_URI = "mongodb+srv://vohoa:vohoa@cluster0.deqp0qk.mongodb.net/vohoa"
    PERMANENT_SESSION_LIFETIME = timedelta(weeks=5)
