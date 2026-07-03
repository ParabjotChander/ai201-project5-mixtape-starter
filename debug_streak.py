from datetime import datetime, timedelta, timezone
from app import create_app
from models import User
from services.streak_service import update_listening_streak

app = create_app()

with app.app_context():
    user = User.query.first()

    last_listened= datetime(2026, 7, 4, tzinfo=timezone.utc)
    # snapshot original values (DO NOT MODIFY DB)
    original_streak = 5
    original_last = last_listened

    print("BEFORE Sunday (Saturday): Listening Streak:", user.listening_streak)
    # simulate Sunday
    now = datetime(2026, 7, 5, tzinfo=timezone.utc)

    # IMPORTANT: work on a COPY, not DB state
    test_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        listening_streak=original_streak,
        last_listened_at=original_last
    )

    print("Simulating Sunday with last listened on Saturday")
    update_listening_streak(test_user, now)

    print("Listening During Sunday, Listening Streak:", test_user.listening_streak)