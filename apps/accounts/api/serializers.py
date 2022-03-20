from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
	image = serializers.SerializerMethodField()
	full_name = serializers.SerializerMethodField()

	class Meta:
		model = get_user_model()
		fields = ('username', 'email', "first_name", "last_name", 'full_name', 'image', 'public_id')
		read_only_fields= [ 'username', 'public_id', 'full_name']

	def get_image(self, obj):
		request = self.context.get('request')
		if obj.image:
			return request.build_absolute_uri(obj.image.url)

		return None

	def get_full_name(self, obj):
		return obj.get_full_name()
