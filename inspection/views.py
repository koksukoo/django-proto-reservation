from rest_framework import viewsets
from rest_framework import permissions
from inspection.serializers import ReservationSerializer
from reservation.models import Reservation

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]