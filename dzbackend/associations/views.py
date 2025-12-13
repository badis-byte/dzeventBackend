from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.supabase_client import supabase

class AssocList(APIView):
    def get(self, request):
        result = supabase.table("associations").select("*").execute()
        return Response(result.data)

class AssocCreate(APIView):
    def post(self, request):
        payload = dict(request.data)
        payload.pop("id", None)  # NEVER send id

        result = supabase.table("associations").insert(payload).execute()
        print(result.data)
        return Response(result.data, status=status.HTTP_201_CREATED)

class AssocDeleteAll(APIView):
    def delete(self, request):
        supabase.table("associations").delete().neq("id", -1).execute()
        return Response({"deleted": True})

class AssocLogin(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        result = (
            supabase.table("associations")
            .select("*")
            .eq("email", email)
            .eq("password", password)
            .execute()
        )

        if not result.data:
            return Response({"error": "Invalid credentials"},
                             #status=400
                             )

        return Response(result.data[0])

class AssocUnverified(APIView):
    def get(self, request):
        result = (
            supabase.table("associations")
            .select("*")
            .eq("isVerified", False)
            .execute()
        )
        print(result.data)
        return Response(result.data)

class AssocDetail(APIView):
    def get(self, request, id):
        result = (
            supabase.table("associations")
            .select("*")
            .eq("id", id)
            .execute()
        )
        return Response(result.data)

class AssocVerify(APIView):
    def patch(self, request, id):
        result = (
            supabase.table("associations")
            .update({"isVerified": True})
            .eq("id", id)
            .execute()
        )
        return Response(result.data)

class AssocDelete(APIView):
    def delete(self, request, id):
        supabase.table("associations").delete().eq("id", id).execute()
        return Response({"deleted": True})

