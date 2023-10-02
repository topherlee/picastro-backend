from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, PicastroUser, SavedImages, Comment


class CreateUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=PicastroUser.objects.all())]
    )

    username = serializers.CharField(
        required=True,
        max_length=25,
        validators=[UniqueValidator(queryset=PicastroUser.objects.all())]
    )

    password = serializers.CharField(
        min_length=6,
        max_length=68,
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
        model = PicastroUser
        fields = ('token', 'username', 'password',
                'first_name', 'last_name', 'email', 'id',)
        write_only_fields = 'password'
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',
                'isEmailVerified', 'isPhoneVerified',) 

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = PicastroUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'last_login', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = PicastroUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'last_login', 'date_joined', 'location', 'userDescription',
                  'genderIdentifier', 'profileImage', 'total_likes', 'phone_no']
        write_only_fields = 'password'

    def get_total_likes(self, obj):
        return SavedImages.objects.filter(user=obj).count()


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicastroUser
        fields = ['id', 'username', 'profileImage', 'location']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image', 'astroNameShort', 'astroName', 'award',
                'exposureTime', 'moonPhase', 'cloudCoverage', 'bortle',
                'pub_date', 'imageDescription',
                'imageCategory', 'poster', 'thumbnail', 'aspectRatio']
        # read_only_fields = ['thumbnail']
        extra_kwargs = {'thumbnail': {'required': False}}

    def to_representation(self, instance):
        self.fields['poster'] = PosterSerializer(read_only=True)
        return super(PostSerializer, self).to_representation(instance)


class LikeImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SavedImages
        fields = ['user', 'post']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment 
        fields = ['post', 'commenter', 'comment_body', 'date_added']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def validate(self, attrs):

        email = attrs['data'].get('email', '')
        
        return super().validate(attrs)
