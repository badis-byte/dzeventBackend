from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.supabase_client import supabase


class InterestCreateView(APIView):
    def post(self, request):
        user_id = request.data.get("userId")
        event_id = request.data.get("eventId")

        if not user_id or not event_id:
            return Response(
                {"error": "user_id and event_id required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = (
            supabase
            .table("interests")
            .insert({
                "userId": user_id,
                "eventId": event_id,
            })
            .execute()
        )

        return Response(result.data, status=status.HTTP_201_CREATED)


class InterestDeleteView(APIView):
    def delete(self, request):
        user_id = request.data.get("userId")
        event_id = request.data.get("eventId")

        if not user_id or not event_id:
            return Response(
                {"error": "user_id and event_id required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        (
            supabase
            .table("interests")
            .delete()
            .eq("userId", user_id)
            .eq("eventId", event_id)
            .execute()
        )

        return Response({"deleted": True})


class UserInterestsView(APIView):
    def get(self, request, user_id):
        result = (
            supabase
            .table("interests")
            .select("userId,eventId,createdAt")
            .eq("userId", user_id)
            .execute()
        )

        return Response(result.data)


class InterestDetailView(APIView):
    def get(self, request, user_id, event_id):
        result = (
            supabase
            .table("interests")
            .select("*")
            .eq("userId", user_id)
            .eq("eventId", event_id)
            .execute()
        )

        if not result.data:
            return Response(
                {"detail": "Not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(result.data[0])


from typing import Any, Mapping, Sequence, cast

from rest_framework.views import APIView
from rest_framework.response import Response

from core.supabase_client import supabase
from postgrest import APIResponse


class UserInterestedEventsView(APIView):
    def get(self, request, user_id: int):
        resp: APIResponse[Any] = (
            supabase
            .table("interests")
            .select("eventId")
            .eq("userId", user_id)
            .execute()
        )

        if not resp.data:
            return Response([])

        # 🔹 Narrow Supabase's weak JSON typing
        interests = cast(Sequence[Mapping[str, Any]], resp.data)

        event_ids = [row["eventId"] for row in interests]

        if not event_ids:
            return Response([])

        events_resp: APIResponse[Any] = (
            supabase
            .table("events")
            .select("*")
            .in_("id", event_ids)
            .execute()
        )

        return Response(events_resp.data or [])


