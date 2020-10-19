from rest_framework import serializers
from reservation.models import Reservation


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time', 'total_price']