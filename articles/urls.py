from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    path("", views.ArticleListAPIView.as_view(), name="article_list"),  # 클래스 기반 view라서 내장된 메서드인 as_view()를 사용해서 view 함수 목록을 제공해줘야 한다.
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:article_pk>/comments/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("comments/<int:comment_pk>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),
    path("check-sql/", views.check_sql, name="check_sql")
]