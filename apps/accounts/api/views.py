import requests
from django.contrib.auth import get_user_model
from django.http import Http404
# from oauth2_provider.contrib.rest_framework import (TokenHasReadWriteScope,
# 													TokenHasScope)
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


class UserView(APIView):
    schema = None
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = self.get_object(request.user.pk)
        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data)
