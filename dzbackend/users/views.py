from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.supabase_client import supabase
from postgrest.exceptions import APIError


class UserList(APIView):
    def get(self, request):
        try:
            result = supabase.table("user").select("*").execute()
            return Response(result.data, status=status.HTTP_200_OK)
        except APIError as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    def post(self, request):
        payload = dict(request.data)
        payload.pop("id", None)  # NEVER send id

        try:
            result = supabase.table("user").insert(payload).execute()
            return Response(result.data[0], status=status.HTTP_201_CREATED)
        except APIError as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            result = (
                supabase.table("user")
                .select("*")
                .eq("email", email)
                .eq("password", password)
                .execute()
            )

            if not result.data:
                return Response(
                    {"error": "Invalid credentials"},
                    #status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(result.data[0], status=status.HTTP_200_OK)

        except APIError as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get(self, request, id):
        try:
            result = (
                supabase.table("user")
                .select("*")
                .eq("id", id)
                .single()
                .execute()
            )
            return Response(result.data, status=status.HTTP_200_OK)
        except APIError as e:
            return Response(e.args, status=status.HTTP_404_NOT_FOUND)


class UserUpdate(APIView):
    def put(self, request, id):
        payload = dict(request.data)
        payload.pop("id", None)

        try:
            result = (
                supabase.table("user")
                .update(payload)
                .eq("id", id)
                .execute()
            )
            return Response(result.data[0], status=status.HTTP_200_OK)
        except APIError as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteAll(APIView):
    def delete(self, request):
        try:
            supabase.table("user").delete().neq("id", -1).execute()
            return Response({"deleted": True}, status=status.HTTP_200_OK)
        except APIError as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)

class UserSetFcmtoken(APIView):
    def post(self, request, id):
        fcmtoken = request.data.get('fcm_token')
        payload = {'user_id': id, 'fcm_token': fcmtoken}
        try:
            result = supabase.table("profiles").insert(payload).execute()
            return Response(status=status.HTTP_201_CREATED)
        except APIError as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)

class UserNotifications(APIView):
    def get(self, request, id):
        try:
            result = supabase.table("notifications").select().eq("user_id", id).execute()
            return Response(result.data, status=status.HTTP_200_OK)
        except APIError as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)