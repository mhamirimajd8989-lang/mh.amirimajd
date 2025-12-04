from peewee import *
from datetime import datetime
import os

# فایل دیتابیس (اگر لازم باشه حذفش می‌کنیم قبل از ساخت جداول)
DB_FILE = "chat.db"

db = SqliteDatabase(DB_FILE)

class BaseModel(Model):
    class Meta:
        database = db

# --------------------------
# 1) جدول User
# --------------------------
class User(BaseModel):
    username = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now)

# --------------------------
# 2) جدول Room
# --------------------------
class Room(BaseModel):
    name = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now)
    created_by = ForeignKeyField(User, backref="created_rooms", null=True)

# --------------------------
# 3) جدول Message
# --------------------------
class Message(BaseModel):
    user = ForeignKeyField(User, backref="messages")
    room = ForeignKeyField(Room, backref="messages")
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

# --------------------------
# 4) جدول PrivateMessageMeta
# --------------------------
class PrivateMessageMeta(BaseModel):
    from_user = ForeignKeyField(User, backref="sent_private_meta")
    to_user = ForeignKeyField(User, backref="received_private_meta")
    created_at = DateTimeField(default=datetime.now)
    is_new_chat = BooleanField(default=True)
    encryption_enabled = BooleanField(default=False)

# --------------------------
# 5) جدول PrivateMessage
# --------------------------
class PrivateMessage(BaseModel):
    meta = ForeignKeyField(PrivateMessageMeta, backref="messages")
    content = TextField()
    created_at = DateTimeField(default=datetime.now)
    is_read = BooleanField(default=False)

# --------------------------
# ساخت جدول‌ها (آخر فایل)
# --------------------------
if __name__ == "__main__":
    # اگر می‌خواهی دیتابیس قبلی رو پاک کنی (توصیه میشه فقط برای توسعه)
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    db.connect()
    db.create_tables([User, Room, Message, PrivateMessageMeta, PrivateMessage])
    db.close()
    print("Tables created successfully.")
