from rest_framework import serializers
from .models import User , Profile

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
# To edit jwt token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.validators import UniqueValidator

####################



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # These are claims, you can add custom claims (data)
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)
        token['verified'] = user.profile.verified
        return token



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'image']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta :
        model = User
        fields = ('id', 'username', 'first_name' , 'last_name' , 'email' , 'profile')
        read_only_fields = ['id']
        def update(self, instance, validated_data):
            ''' method to update user an profile '''
            profile_data = validated_data.pop('profile', {})
            profile = instance.profile
            # update user data
            instance.username = validated_data.get('username', instance.username)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('username', instance.last_name)
            instance.email = validated_data.get('email', instance.email)
            instance.save()
            # update profile data
            profile.full_name = profile_data.get('full_name', profile.full_name)
            profile.bio = profile_data.get('bio', profile.bio)
            profile.image = profile_data.get('image', profile.image)
            profile.save()
            return instance
        # if u but fields = ('id', 'username', 'email' , 'password')
        # maybe will return the password , to make it write only and cant return it write this
        # extra_kwargs = {'password': {'write_only': True, 'required': True}}







class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    def validate(self, data):
        """ check the data """
        user = self.context['request'].user
        # check old password
        if not check_password(data['old_password'], user.password):
            raise serializers.ValidationError({"old_password": "wrong password"})
        # to make sure the user write new password
        elif data['new_password'] == data['old_password']:
            raise serializers.ValidationError({"confirm_password": "new password is same old password "})
        # check password1 and password2
        elif data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "password updated"})
        return data
    def update_password(self, user):
        """ update password for the current user """
        user.set_password(self.validated_data['new_password'])
        user.save()





class RegisterSerializer(serializers.ModelSerializer):
    '''Serializer for user registration.
    This serializer is responsible for handling user registration by
    validating passwords, ensuring password confirmation, and creating
    a new user with a hashed password.
    '''
    # Define password field, making it write-only and required, with password validation
    password = serializers.CharField(write_only=True, required=True ,validators=[validate_password])
    # Define password2 (confirmation password) with the same constraints as password
    password2 = serializers.CharField(write_only=True, required=True , validators=[validate_password])
    class Meta:
        '''
        Meta class specifying the model and fields to be included in the serializer.
        '''
        model = User
        # Fields to be handled
        fields = ('email', 'username', 'first_name' , 'last_name' , 'password', 'password2')
    def validate(self, attrs):
        '''
        Validate that password and password2 match.
        Raises:
            serializers.ValidationError: If the two password fields do not match.
        '''
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError( {"password": "Password fields didn't match."} )
        # Return validated data if passwords match
        return attrs
    def create(self, validated_data):
        '''
        Create and return a new user instance after hashing the password.
        Args:
            validated_data (dict): The validated user data.
        Returns:
            User: The created user instance.
        '''
        # Create user instance without setting the password directly ( save the data )
        user = User.objects.create(username=validated_data['username'],first_name=validated_data['first_name'],last_name=validated_data['last_name'],email=validated_data['email'])
        # Hash the password before saving the user
        user.set_password(validated_data['password'])
        # Save the user to the database
        user.save()
        # Then return the created user instance
        return user
