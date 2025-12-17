from datetime import datetime, timezone
from core.supabase_client import supabase

def notify_close_events():
    # Fetch events
    result = supabase.table("events").select("*").execute()
    if not result.data:
        raise Exception("(Events::tasks::notify_close_events) Failed to fetch events")

    events = result.data

    now = datetime.now()

    for event in events:
        # Parse datetime (assuming ISO strings in DB)
        end_dt = datetime.fromisoformat(event["endDatetime"])

        days_left = (end_dt - now).days

        # Skip if more than 1 day left or already finished
        if days_left != 1:
            continue

        # Fetch interested users
        interests_res = (
            supabase
            .table("interests")
            .select("userId")
            .eq("eventId", event["id"])
            .execute()
        )

        if not interests_res.data:
            continue

        for interest in interests_res.data:
            notif_payload = {
                "user_id": interest["userId"],
                "body": f"One day left to the event: {event['title']}"
            }

            supabase.table("notifications").insert(notif_payload).execute()
