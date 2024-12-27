
# 이제는 클래스 기반으로 뷰를 작성해보자.(CBV)

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Article, Comment
from .serializers import (
    ArticlesSerializer,
    ArticlesDetailSerializer,
    CommentSerializer)

class ArticleListAPIView(APIView):

    permission_classes = [IsAuthenticated]  # 이 class 안에서는 항상 IsAuthenticated 된 permission을 사용할 것이다.
    # 즉, 이 코드 한 줄만 가지고도, get이든 post든 어떤 요청을 보낼 때마다 header에 Token을 넣어줘야 동작하게 된다.

    @extend_schema(
            tags=['Articles'],
            description="Article 목록 조회를 위한 API",
    )
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticlesSerializer(articles, many=True)    # 1개의 데이터가 아니라, 더 많은 데이터를 가져올 때는 꼭 many=True 옵션을 넣어야 한다.
        return Response(serializer.data)
    
    @extend_schema(
            tags=['Articles'],
            description="Article 생성을 위한 API",
            request=ArticlesSerializer,
    )
    def post(self, request):
        serializer = ArticlesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):   # raise_exception=True 하면, 아래에 주석처리한 (return Response(serializer.errors, status=400))를 알아서 내부적으로 해준다.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    # 200은 그냥 성공, 201은 생성되었다는 의미를 가짐.
        # return Response(serializer.errors, status=400)  # () 안에 serializer.errors를 빼도 되고 아무거나 넣어도 되지만, 이렇게 하면 왜 is_valid()하지 않은지 이유가 나온다.
        # 400번은 Bad Request. 클라이언트가 제목이 빠졌든지 글자 수가 넘었든지, 등등.

class ArticleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticlesDetailSerializer(article)
        return Response(serializer.data)
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticlesDetailSerializer(article, data=request.data, partial=True)
        # 생성할 때는 title과 content 모두 꼭 적어야 했는데, 수정할 때는 수정하고 싶은 것만 수정할 수 있게 partial=True 옵션을 넣었다.
        # 이러면 title 없이 content만 수정하거나 할 수 있게 된다.
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, article_pk):
        get_object_or_404(Article, pk=article_pk)

    def get(self, request, article_pk):
        article = self.get_object(article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, article_pk):
        article = self.get_object(article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, comment_pk):
        get_object_or_404(Comment, pk=comment_pk)

    # 댓글 수정
    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)  # comment는 content만 넣기 때문에 partial=True 옵션은 안 넣어줘도 된다. 넣어줘도 된다!
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # 댓글 삭제
    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def check_sql(request):

    comments = Comment.objects.all().prefetch_related("article")
    for comment in comments:
        print(comment.article.title)

    return Response()