##from supabase import create_client
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.supabase_client import supabase
from postgrest.exceptions import APIError
import json
import mimetypes

from .tasks import notify_close_events

class EventListCreate(APIView):
    """Get all events or create a new event"""

    def get(self, request):
        try:
            result = supabase.table("events").select("*").execute()
            return Response(result.data or [], status=status.HTTP_200_OK)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = {
            "createdAt": request.data.get("createdAt"),
            "title": request.data.get("title"),
            "description": request.data.get("description"),
            "location": request.data.get("location"),
            "associationId": request.data.get("associationId"),
            "category": request.data.get("category"),
            "endDatetime": request.data.get("endDatetime"),
            "startDatetime": request.data.get("startDatetime"),
            "imageUrl": request.data.get("imageUrl"),
        }
        #data.pop("id", None)
        data["associationId"] = int(data["associationId"])

        image = request.FILES.get("image")

        # Validate required fields
        # required_fields = ["title", "date"]
        # for field in required_fields:
        #     if field not in data:
        #         return Response(
        #             {"error": f"{field} is required"},
        #             status=status.HTTP_400_BAD_REQUEST,
        #         )

        # Upload image to Supabase (if provided)
        if image:
            path = data["imageUrl"]

            content_type = image.content_type
            if content_type == "application/octet-stream" or not content_type:
                guessed, _ = mimetypes.guess_type(image.name)
                content_type = guessed or "image/jpeg"

            try:
                # supabases = create_client(
                #     "https://jkcqgchkidxxtrjhmmha.supabase.co",
                #     "58c924d872df7380f4d00ba169a7c0d1ced53e5dc524d8a3c15af5ebc3deef82"
                # )
                supabase.storage.from_("pictures").upload(
                    path="events/"+path,
                    file=image.read(),
                    file_options={"content-type": content_type},
                )

                data["imageUrl"] = supabase.storage.from_("pictures").get_public_url("events/"+path)
                result = supabase.table("events").insert(dict(data)).execute()
            except APIError as e:
        # Insert clean data into Supabase
                print("------2222222----------"+e)

        return Response(result.data, status=status.HTTP_201_CREATED)


class EventDetail(APIView):
    """Retrieve, update, or delete a single event by ID"""

    def get(self, request, id):
        try:
            result = supabase.table("events").select("*").eq("id", id).single().execute()
            if not result.data:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(result.data, status=status.HTTP_200_OK)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            payload = json.loads(request.body.decode("utf-8"))
            result = supabase.table("events").update(payload).eq("id", id).execute()
            return Response(result.data, status=status.HTTP_200_OK)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            supabase.table("events").delete().eq("id", id).execute()
            return Response({"deleted": True}, status=status.HTTP_200_OK)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteAll(APIView):
    """Delete all events"""

    def delete(self, request):
        try:
            supabase.table("events").delete().neq("id", -1).execute()
            return Response({"deleted": True}, status=status.HTTP_200_OK)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EventFilteredList(APIView):
    """Get events filtered by category"""

    def post(self, request):
        try:
            payload = json.loads(request.body.decode("utf-8"))
            filters = payload.get("categories", [])
            if not filters:
                result = supabase.table("events").select("*").execute()
            else:
                # Build OR query for multiple categories
                query = supabase.table("events").select("*")
                for i, cat in enumerate(filters):
                    query = query.or_(f"category.eq.{cat}" if i == 0 else f"or=category.eq.{cat}")
                result = query.execute()
            return Response(result.data or [], status=status.HTTP_200_OK)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EventSearch(APIView):
    """Search events by title"""

    def get(self, request):
        try:
            search_str = request.query_params.get("q", "")
            if not search_str:
                return Response([], status=status.HTTP_200_OK)
            result = supabase.table("events").select("*").ilike("title", f"%{search_str}%").execute()
            return Response(result.data or [], status=status.HTTP_200_OK)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class EventUserList(APIView):
    """Get all events posted by a specific user/association"""

    def get(self, request, user_id):
        try:
            result = supabase.table("events").select("*").eq("associationId", user_id).execute()
            return Response(result.data or [], status=status.HTTP_200_OK)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NotifyCloseEvent(APIView):
    def get(self, request):
        try:
            notify_close_events()
            return Response(status=status.HTTP_200_OK)
        except APIError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)