from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from Craftsman.models import Craftman
from BusinessPartner.models import BusinessPartner


class CraftmanSerializer(serializers.ModelSerializer):
    """
    Serializer for Craftman model with custom permission fields.
    """
    bp_code = serializers.SlugRelatedField(
        queryset=BusinessPartner.objects.all(),
        slug_field='bp_code',
        required=False,
        allow_null=True
    )

    user_permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, required=False
    )
    
    # Permission fields
    view_only = serializers.BooleanField(default=False)
    copy = serializers.BooleanField(default=False)
    screenshot = serializers.BooleanField(default=False)
    print_perm = serializers.BooleanField(default=False)
    download = serializers.BooleanField(default=False)
    share = serializers.BooleanField(default=False)
    edit = serializers.BooleanField(default=False)
    delete = serializers.BooleanField(default=False)
    manage_roles = serializers.BooleanField(default=False)
    approve = serializers.BooleanField(default=False)
    reject = serializers.BooleanField(default=False)
    archive = serializers.BooleanField(default=False)
    restore = serializers.BooleanField(default=False)
    transfer = serializers.BooleanField(default=False)
    custom_access = serializers.BooleanField(default=False)
    full_control = serializers.BooleanField(default=False)
    delete_flag = serializers.BooleanField(default=False)

    class Meta:
        model = Craftman
        fields = [
            'id', 'profile_picture', 'user_code', 'bp_code', 'full_name', 'email_id', 'mobile_no',
            'company_name', 'password', 'user_state', 'status', 'dob', 'gender',
            'city', 'state', 'country', 'pincode', 'created_at', 'updated_at', 'user_permissions',
            'view_only', 'copy', 'screenshot', 'print_perm', 'download', 'share', 'edit', 'delete', 
            'manage_roles', 'approve', 'reject', 'archive', 'restore', 'transfer', 'custom_access', 
            'full_control', 'delete_flag',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def to_representation(self, instance):
        """Modify the output representation to include business_name with bp_code."""
        data = super().to_representation(instance)
        
        # Add BP details if bp_code exists
        if instance.bp_code:
            data['bp_code'] = f"{instance.bp_code.bp_code}-{instance.bp_code.business_name}"
            bp = BusinessPartner.objects.filter(bp_code=instance.bp_code.bp_code).first()
            if bp:
                data['bp_email'] = bp.email
                data['bp_mobile'] = bp.mobile
                data['bp_full_name'] = bp.full_name
        
        return data
    
    def get_permissions(self, obj):
        """Get user-specific permissions."""
        user_permissions = obj.user_permissions.all()
        return [{'codename': perm.codename, 'name': perm.name, 'granted': True} for perm in user_permissions]

    def validate_groups(self, value):
        """Validate group IDs."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Groups must be provided as a list.")

        groups = []
        for group_id in value:
            try:
                group = Group.objects.get(id=group_id)
                groups.append(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError(f"Group with ID {group_id} does not exist.")
        return groups

    def generate_user_code(self):
        """
        Generate user_code with CF prefix for Craftsman.
        """
        prefix = "CF"  # Fixed prefix for Craftsman
        last_user = Craftman.objects.filter(user_code__startswith=prefix + "-").order_by('-user_code').first()
        
        if last_user:
            last_number = int(last_user.user_code.split('-')[1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"{prefix}-{new_number:04d}"

    def create(self, validated_data):
        """
        Create Craftsman user with auto-generated user_code.
        """
        # Generate user code with CF prefix
        validated_data['user_code'] = self.generate_user_code()
        
        # Handle password
        password = validated_data.pop('password', None)
        
        # Handle groups
        groups = validated_data.pop('groups', [])
        
        # Create user
        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        if groups:
            user.groups.set(groups)

        return user

    def update(self, instance, validated_data):
        """
        Update Craftsman user.
        """
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save(update_fields=['password'])

        if groups is not None:
            instance.groups.set(groups)

        return instance