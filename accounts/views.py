from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.models import LogmanUser
from accounts.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
class UserViewSet(viewsets.ModelViewSet):
    queryset = LogmanUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def get_by_email(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = LogmanUser.objects.get(email=email)
        except LogmanUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)