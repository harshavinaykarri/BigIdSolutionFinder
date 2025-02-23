from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    Items Views
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
