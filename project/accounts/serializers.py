from rest_framework import serializers
from .models import User , Profile

from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

####################



class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('id', 'username', 'email')
        # if u but fields = ('id', 'username', 'email' , 'password')
        # maybe will return the password , to make it write only and cant return it write this
        # extra_kwargs = {'password': {'write_only': True, 'required': True}}




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




class RegisterSerializer(serializers.ModelSerializer):
    '''Serializer for user registration.
    This serializer is responsible for handling user registration by
    validating passwords, ensuring password confirmation, and creating
    a new user with a hashed password.
    '''
    # Define password field, making it write-only and required, with password validation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # Define password2 (confirmation password) with the same constraints as password
    password2 = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        '''
        Meta class specifying the model and fields to be included in the serializer.
        '''
        model = User
        # Fields to be handled
        fields = ('email', 'username', 'password', 'password2')

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
        user = User.objects.create( username=validated_data['username'] , email=validated_data['email'] )
        # Hash the password before saving the user
        user.set_password(validated_data['password'])
        # Save the user to the database
        user.save()
        # Then return the created user instance
        return user
