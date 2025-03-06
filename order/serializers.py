from rest_framework import serializers
from .models import Order
from user.models import ResUser  


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Order model.
    """
    class Meta:
        model = Order
        fields = [
            'id', 'bp_code', 'name', 'reference_no', 'order_date', 'due_date', 'category', 'order_type',
            'quantity', 'weight', 'dtype', 'branch_code', 'product', 'design', 'vendor_design', 'barcoded_quality',
            'supplied', 'balance', 'assigned_by', 'narration', 'note', 'sub_brand', 'make', 'work_style', 'form',
            'finish', 'theme', 'collection', 'description', 'assign_remarks', 'screw', 'polish', 'metal_colour',
            'purity', 'stone', 'hallmark', 'rodium', 'enamel', 'hook', 'size', 'open_close', 'length', 'hbt_class',
            'console_id', 'tolerance_from', 'tolerance_to', 'order_image'
        ]
        # read_only_fields = [ 'bp_code', 'order_date']

    def create(self, validated_data):
        """
        Custom create method to handle the creation of the Order instance.
        """
        request = self.context.get('request')
        user = request.user if request else None
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("User not authenticated")
        
        validated_data.setdefault('state', 'draft')  # Ensure state defaults to 'draft'
        order = Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        """
        Custom update method to handle updates to the Order instance.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class OrderUpdateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=[
        ('accepted', 'Accepted'), ('rejected', 'Rejected')
    ])
    text = serializers.CharField(max_length=255, required=False)
    selection = serializers.ChoiceField(choices=[], required=False)
    flag = serializers.HiddenField(default='flag')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = ResUser.objects.filter(role_name='craftsman')
        if self.context.get('state') != 'rejected':
            self.fields['selection'].choices = [(user.id, user.username) for user in users]
        else:
            self.fields.pop('selection', None)


class BackSellerOrderUpdateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=[
        ('accepted', 'Accepted'), ('rejected', 'Rejected')
    ])
    text = serializers.CharField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)









# from rest_framework import serializers
# from .models import Order
# from user.models import ResUser # Ensure correct capitalization for class names


# class OrderSerializer(serializers.ModelSerializer):
#     """
#     Serializer class for the Order model.
#     """
#     class Meta:
#         model = Order
#         fields = [
#             'id', 'order_no', 'category', 'quantity', 'weight', 'weight_unit',
#             'size', 'stone', 'rodium', 'hallmark', 'screw', 'hook',
#             'narration', 'order_image', 'due_date', 'created_at', 'updated_at'
#         ]
#         read_only_fields = ['order_no', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         """
#         Custom create method to handle the creation of the Order instance.
#         """
#         print(self.context.get('request').user,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")

#         user = self.context.get('request').user if self.context.get('request')  else None
#         if user is None:
#             raise serializers.ValidationError("User not authenticated")
#         validated_data['user_id'] = user

#     # Ensure the state is set to "draft" by default
        
#         validated_data.setdefault('state', 'draft')
#         order = Order.objects.create(**validated_data)
#         return order

#     def update(self, instance, validated_data):
#         """
#         Custom update method to handle updates to the Order instance.
#         """
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()  # Ensure the `save` method in the model is called for consistency
#         return instance


# class OrderUpdateSerializer(serializers.Serializer):
#     state = serializers.ChoiceField(choices=['accepted', 'rejected'])
#     text = serializers.CharField(max_length=255, required=False)
#     selection = serializers.ChoiceField(choices=[], required=False)  # Initially empty
#     flag = serializers.HiddenField(default='flag')  # Hidden field to ensure the serializer is valid
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Dynamically populate the selection field with all users if the state is "accepted"
#         users = ResUser.objects.filter(role_name='craftsman')
#         if not self.context.get('state') == 'rejected':
#             self.fields['selection'].choices = [(user.id, user.username) for user in users]
#         else:
#             self.fields.pop('selection') or None 



# class BackSellerOrderUpdateSerializer(serializers.Serializer):
#     state = serializers.ChoiceField(choices=['accepted', 'rejected'])
#     text = serializers.CharField()
#     start_date = serializers.DateField(required=False)
#     end_date = serializers.DateField(required=False)
    
#     # selection = serializers.ChoiceField(choices=[], required=False)  # Initially empty
#     # flag = serializers.HiddenField(default='flag')  # Hidden field to ensure the serializer is valid
#     # def __init__(self, *args, **kwargs):
#         # super().__init__(*args, **kwargs)
#         # Dynamically populate the selection field with all users if the state is "accepted"
#         # users = ResUser.objects.filter(role_name='craftsman')
#         # if not self.context.get('state') == 'rejected':
#             # self.fields['selection'].choices = [(user.id, user.username) for user in users]
#         # else:
#             # self.fields.pop('selection') or None 
