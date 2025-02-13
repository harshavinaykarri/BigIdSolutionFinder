from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    """
    Item Serializer
    """
    class Meta:
        """
        Meta calss of what to return
        """
        model = Item
        fields = '__all__'

        def create(self,validated_data):
            """
            Create Entries in Table.
            """
            env = Item.objects.create(**validated_data)
            return env
