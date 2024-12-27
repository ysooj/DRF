from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("article",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("article")
        return ret

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

class ArticlesDetailSerializer(ArticlesSerializer):
    # comments는 models.py에서 설정해준 이름으로, 역참조로 article에서 comment를 참조하는 것이다. 이를 이용해서 Nested Relationships(포함 관계) 해줄 수 있다.
    comments = CommentSerializer(many=True, read_only=True) # read_only=True 해주지 않으면, POST할 때 문제가 생긴다.
    # 이렇게 추가해주는 field들은 Meta 클래스 안쪽에 read_only_fields로 넣어주는 게 아니라,
    # 각각의 field에 read_only=True 로 넣어주어야 한다.
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)