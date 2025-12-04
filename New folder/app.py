from datetime import datetime
from models import User, Room, Message, PrivateMessage, PrivateMessageMeta

# --------------------------
# ایجاد کاربر
# --------------------------
def create_user(username):
    return User.create(username=username)

# --------------------------
# ایجاد روم
# --------------------------
def create_room(name, owner):
    return Room.create(name=name, created_by=owner)

# --------------------------
# ارسال پیام عمومی
# --------------------------
def send_message(user, room, content):
    return Message.create(user=user, room=room, content=content)

# --------------------------
# ایجاد چت خصوصی
# --------------------------
def create_private_chat(user1, user2, is_encrypted=False):
    return PrivateMessageMeta.create(
        from_user=user1,
        to_user=user2,
        created_at=datetime.now(),
        encryption_enabled=is_encrypted
    )

# --------------------------
# ارسال پیام خصوصی
# --------------------------
def send_private_message(meta, content):
    return PrivateMessage.create(
        meta=meta,
        content=content,
        created_at=datetime.now(),
        is_read=False
    )

# --------------------------
# نمایش پیام‌های یک روم
# --------------------------
def show_room_messages(room):
    for msg in Message.select().where(Message.room == room):
        print(f"{msg.user.username}: {msg.content}")

# --------------------------
# نمایش پیام‌های خصوصی
# --------------------------
def show_private_messages(meta):
    for pm in PrivateMessage.select().where(PrivateMessage.meta == meta):
        print(f"{pm.content}")

# --------------------------
# نمونه استفاده
# --------------------------
if __name__ == "__main__":
    user1 = create_user("Alice")
    user2 = create_user("Bob")

    room = create_room("General", user1)
    send_message(user1, room, "سلام همه!")
    send_message(user2, room, "سلام آلیس!")

    show_room_messages(room)

    chat_meta = create_private_chat(user1, user2)
    send_private_message(chat_meta, "سلام بوب، حالت چطوره؟")
    send_private_message(chat_meta, "خوبم!")

    show_private_messages(chat_meta)
