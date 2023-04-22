from rest_framework import serializers
from .models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    userId = serializers.ReadOnlyField(source="userId.id")
    username = serializers.ReadOnlyField(source="userId.username")
    profilePicUrl = serializers.ImageField(source="userId.profilePicUrl", read_only=True)
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()

    class Meta:
        model=Post
        fields = [
            "id",
            "caption",
            "description",
            "postPicUrl",
            "created_at",
            "updated_at",
            "total_likes",
            "total_comments",
            "has_liked",
            "userId",
            "username",
            "profilePicUrl",
            "urls",
        ]
        extra_kwargs={"userId": {"write_only":True}}
    
    def get_total_likes(self, post):
        """
        Get total no. of likes on the post.
        """
        if not self.context: return 0
        return post.like_post.count()
    
    def get_total_comments(self, post):
        """
        Get total no. of comments on the post.
        """
        if not self.context: return 0
        return post.comment_post.count()

    def get_has_liked(self, post):
        """
        Check if current user has liked the post or not.
        """
        if not self.context: return False
        liked_post_of_user = self.context.get("liked_post_of_user")
        return True if post.id in liked_post_of_user else False
    
    def get_urls(self, post):
        """
        Get useful urls
        """
        if not self.context: return None
        like_info_url = "/apis/v1/posts/like-info/%s/" % post
        comment_info_url = "/apis/v1/posts/comment-info/%s/" % post
        urls = {
            "like_info_url": like_info_url,
            "comment_info_url": comment_info_url,
        }
        return urls


class LikeSerializer(serializers.ModelSerializer):
    userId = serializers.ReadOnlyField(source="liked_by_id")
    username = serializers.ReadOnlyField(source="liked_by.username")
    profilePicUrl = serializers.ImageField(source="liked_by.profilePicUrl", read_only=True)

    class Meta:
        model = Like
        fields = [
            "id",
            "userId",
            "username",
            "profilePicUrl"
        ]
    

class CommentSerializer(serializers.ModelSerializer):
    userId = serializers.ReadOnlyField(source="commented_by_id")
    username = serializers.ReadOnlyField(source="commented_by.username")
    profilePicUrl = serializers.ImageField(source="commented_by.profilePicUrl", read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "created_at",
            "userId",
            "username",
            "profilePicUrl"
        ]