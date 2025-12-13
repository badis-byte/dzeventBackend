from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.supabase_client import supabase
#from postgrest.enums import CountMethod

class FollowersCountView(APIView):
    def get(self, request, assoc_id):
        resp = supabase.table("followers").select("*", count="exact")  # type: ignore
        resp = resp.eq("associationId", assoc_id).execute()

        return Response({"count": resp.count or 0})

class FollowUnfollowView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        assoc_id = request.data.get("association_id")
        if not user_id or not assoc_id:
            return Response({"error": "user_id and association_id required"}, status=400)
        resp = supabase.table("followers").insert({
            "userId": user_id,
            "associationId": assoc_id,
            "notify": True
        }).execute()
        return Response(resp.data, status=201)

    def delete(self, request):
        user_id = request.data.get("user_id")
        assoc_id = request.data.get("association_id")
        if not user_id or not assoc_id:
            return Response({"error": "user_id and association_id required"}, status=400)
        supabase.table("followers").delete().eq("userId", user_id).eq("associationId", assoc_id).execute()
        return Response({"deleted": True})

class FollowedAssociationsView(APIView):
    def get(self, request, user_id):
        resp = (
            supabase
            .table("followers")
            .select("*")  # return id, userId, associationId, notify
            .eq("userId", user_id)
            .execute()
        )
        data = resp.data or []

        return Response(data)

