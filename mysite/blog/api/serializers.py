from rest_framework.serializers import Serializer, ModelSerializer

from blog.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'blog_title',
            'slug_title',
            'create_date_time',
            'update_date_time',
            'blog_content',
            # 'blog_comment', # Object of type 'GenericRelatedObjectManager' is not JSON serializable
            'blog_author',
            # 'blog_tag',
        ]

