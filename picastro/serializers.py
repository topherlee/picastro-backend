from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, UserProfile

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined']
        

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'location', 'userDescription', 'genderIdentifier', 'profileImage']
        

class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PostSerializer(serializers.ModelSerializer):
    #poster = PosterSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'image', 'astroNameShort', 'astroName', 'imageIsSaved', 
                'award', 'exposureTime', 'moonPhase', 'cloudCoverage', 'bortle',
                'starCamp', 'leadingLight', 'pub_date', 'imageDescription', 
                'imageCategory','poster')
    
    def to_representation(self, instance):
        self.fields['poster'] =  PosterSerializer(read_only=True)
        return super(PostSerializer, self).to_representation(instance)


class CreateUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        required=True,
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    first_name = serializers.CharField(
        required=True
    )

    last_name = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ('token','username', 'password', 'first_name', 'last_name', 'email', 'id',)
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }