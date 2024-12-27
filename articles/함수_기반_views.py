

# 지금까지는 함수 기반으로 뷰를 작성했다. 이제는 클래스 기반으로 뷰를 작성할거다.
# 클래스 기반이 유지보수가 더 용이하고, 우리가 직접 작성하는 코드 수가 적어진다.
# 함수 기반에서 클래스 기반으로 수정한 views.py는 이 앱 디렉토리의 views.py다.


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Article
from .serializers import ArticlesSerializer


# HTTP_STATUS_201_CREATED = 201   # 25번째 줄에서, 에러를 명시적으로 적기 위해서 그냥 숫자만 적는 게 아니라 이렇게 변수 처리해서 에러를 적어준다.
# rest_framework 안쪽에 status라는 곳에 이게 다 들어있다. 그래서 그냥 HTTP_STATUS_201_CREATED 라고 쓰는 게 아니라
# imports로 불러와서 status.HTTP_STATUS_201_CREATED 라고 써야 한다.


@api_view(["GET", "POST"])
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ArticlesSerializer(articles, many=True)    # 1개의 데이터가 아니라, 더 많은 데이터를 가져올 때는 꼭 many=True 옵션을 넣어야 한다.
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = ArticlesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):   # raise_exception=True 하면, 아래에 주석처리한 (return Response(serializer.errors, status=400))를 알아서 내부적으로 해준다.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_STATUS_201_CREATED)    # 200은 그냥 성공, 201은 생성되었다는 의미를 가짐.
        # return Response(serializer.errors, status=400)  # () 안에 serializer.errors를 빼도 되고 아무거나 넣어도 되지만, 이렇게 하면 왜 is_valid()하지 않은지 이유가 나온다.
        # 400번은 Bad Request. 클라이언트가 제목이 빠졌든지 글자 수가 넘었든지, 등등.

@api_view(["GET", "PUT", "DELETE"])
def article_detail(request, pk):
    if request.method == 'GET':
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticlesSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticlesSerializer(article, data=request.data, partial=True)
        # 생성할 때는 title과 content 모두 꼭 적어야 했는데, 수정할 때는 수정하고 싶은 것만 수정할 수 있게 partial=True 옵션을 넣었다.
        # 이러면 title 없이 content만 수정하거나 할 수 있게 된다.
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
                        # 괄호 안에 아무것도 안 적어도 된다. 이게 원래 약속.
                        # 아무것도 안 적으면 200 ok라는 뜻.
                        # 그러나 우리는 배우는 입장이니까 204를 써보는 것.