from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from user.models import ResUser
import random

class ResUserSerializer(serializers.ModelSerializer):
    """
    Serializer for ResUser model, handling dynamic permissions.
    """
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)
    user_permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = ResUser
        fields = [
            'id', 'user_code', 'profile_picture', 'full_name', 'mobile_no', 'email_id', 'password',
            'role_name', 'user_state', 'country', 'state', 'city', 'pincode', 'status', 'dob', 'gender',
            'groups', 'user_permissions', 'permissions', 'created_at', 'updated_at',
            'view_only', 'copy', 'print_perm', 'download', 'share', 'screenshot',
            'edit', 'delete_perm', 'manage_roles', 'approve', 'reject', 'archive',
            'restore_perm', 'transfer', 'custom_access', 'full_control', 'delete_flag'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def get_permissions(self, obj):
        """
        Dynamically fetch the permissions assigned to the user.
        """
        return [
            {'codename': perm.codename, 'name': perm.name, 'granted': perm in obj.user_permissions.all()}
            for perm in Permission.objects.all()
        ]
    
    
    # def get_permissions(self, obj):
    #     """
    #     Dynamically fetch the permissions assigned to the user, including both direct and group-based permissions.
    #     """
    #     user_permissions = set(obj.user_permissions.all())
    #     group_permissions = set(Permission.objects.filter(group__in=obj.groups.all()))
        
    #     all_permissions = user_permissions | group_permissions
        
    #     return [
    #         {'codename': perm.codename, 'name': perm.name}
    #         for perm in all_permissions
    #     ]
        

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     user_permissions = validated_data.pop('user_permissions', [])
    #     validated_data['username'] = validated_data.get(
    #         'username', f"User{random.randint(1000, 9999)}"
    #     )
    #     validated_data.pop('groups', None)
    #     user = super().create(validated_data)
        
    #     if password:
    #         user.set_password(password)
    #         user.save(update_fields=['password'])
    #     if not user_permissions:
    #         user_permissions = list(Permission.objects.all())
    #     user.user_permissions.set(user_permissions)
    #     new_group, created = Group.objects.get_or_create(name="DefaultUserGroup")
    #     new_group.permissions.set(user_permissions)
    #     user.groups.clear()
    #     user.groups.add(new_group)
    #     user.assign_role_permissions()
    #     user.refresh_from_db()
    #     return user


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['permissions'] = self.get_permissions(instance)
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_permissions = validated_data.pop('user_permissions', [])
        groups = validated_data.pop('groups', [])

        validated_data['username'] = validated_data.get(
            'username', f"User{random.randint(1000, 9999)}"
        )

        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        if user_permissions:
            user.user_permissions.set(user_permissions)
        else:
            user_permissions = list(Permission.objects.all())
            user.user_permissions.set(user_permissions)

        user.groups.clear()
        if groups:
            user.groups.set(groups)
        else:
            new_group, created = Group.objects.get_or_create(name="DefaultUserGroup")
            new_group.permissions.set(user_permissions)
            user.groups.add(new_group)

        if hasattr(user, 'assign_role_permissions'):
            user.assign_role_permissions()

        user.refresh_from_db()
        return user




    def update(self, instance, validated_data):
        """
        Override update method to hash password if provided and handle permissions.
        """
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save(update_fields=['password'])

        assigned_permissions = validated_data.get('user_permissions', [])
        if not assigned_permissions:
            assigned_permissions = list(Permission.objects.all())

        instance.user_permissions.set(assigned_permissions)
        new_group_name = f"UserGroup_{instance.id}"
        new_group, created = Group.objects.get_or_create(name=new_group_name)
        new_group.permissions.set(assigned_permissions)

        instance.groups.clear()
        instance.groups.add(new_group)
        instance.assign_role_permissions()
        return instance


class ResAdminUserSerializer(ResUserSerializer):
    """
    Serializer for Admin users with additional permissions.
    """
    class Meta:
        model = ResUser
        fields = ResUserSerializer.Meta.fields


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email_or_mobile = serializers.CharField(max_length=255)
    user_code = serializers.CharField(max_length=25, required=False)
    password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Validate email/mobile and password, and auto-fetch user_code.
        """
        email_or_mobile = data.get('email_or_mobile')
        password = data.get('password')

        if not email_or_mobile or not password:
            raise serializers.ValidationError("Email/mobile and password are required.")

        try:
            if '@' in email_or_mobile:
                user = ResUser.objects.get(email_id=email_or_mobile)
            else:
                user = ResUser.objects.get(mobile_no=email_or_mobile)
            
            data['user_code'] = user.user_code
        except ResUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email/mobile number or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email/mobile number or password.")

        if user.status != 'active':
            raise serializers.ValidationError("This account is inactive. Please contact support.")

        return data
