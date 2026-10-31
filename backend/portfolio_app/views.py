from django.db.models import Count, F, Sum
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, ContactMessage, Education, Experience, Post, PostLike, Profile, Project, Skill, Tag
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    ContactMessageSerializer,
    EducationSerializer,
    ExperienceSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostWriteSerializer,
    ProfileSerializer,
    ProjectSerializer,
    SkillSerializer,
    TagSerializer,
)
from .throttling import AnonymousRateThrottle, CommentCreateThrottle, ContactCreateThrottle, LikeToggleThrottle


class ProjectPagination(PageNumberPagination):
    page_size = 9


class PostPagination(PageNumberPagination):
    page_size = 6


class CommentPagination(PageNumberPagination):
    page_size = 10


class ContactPagination(PageNumberPagination):
    page_size = 10


class CustomTokenObtainPairView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            return Response({'detail': 'No active account found with the given credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {'id': user.id, 'username': user.username, 'email': user.email},
        })


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'is_superuser': request.user.is_superuser,
        })


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            return Response({'detail': 'Both old_password and new_password are required.'}, status=400)
        if not request.user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=400)
        request.user.set_password(new_password)
        request.user.save()
        return Response({'detail': 'Password changed successfully.'})


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        obj, _ = Profile.objects.get_or_create(
            id=1,
            defaults={
                'full_name': 'Md. Ehsanul Islam',
                'headline': 'Full-Stack Developer',
                'bio': 'I build thoughtful digital products and reliable APIs for modern businesses.',
                'email': 'ehsanul@example.com',
                'location': 'Dhaka, Bangladesh',
                'years_of_experience': 2,
            },
        )
        return obj


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('display_order', 'name')
    serializer_class = SkillSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name']
    ordering_fields = ['display_order', 'proficiency']


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all().order_by('-start_date', 'display_order')
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all().order_by('-end_year', '-start_year')
    serializer_class = EducationSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('display_order', '-completed_date')
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ProjectPagination
    filterset_fields = ['category', 'is_featured']
    search_fields = ['title', 'summary', 'description']
    ordering_fields = ['-completed_date', 'display_order']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        tech = self.request.query_params.get('tech')
        if tech:
            queryset = queryset.filter(tech_stack__name__icontains=tech)
        return queryset.distinct()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('category', 'author').prefetch_related('tags', 'likes', 'comments').all()
    serializer_class = PostListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PostPagination
    filterset_fields = ['category__slug', 'tags__slug', 'is_featured']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['-published_at', '-views_count', '-likes_count', 'title']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostWriteSerializer
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def get_queryset(self):
        qs = self.queryset
        if not self.request.user.is_authenticated or not self.request.user.is_superuser:
            qs = qs.filter(status='PUBLISHED')
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        tag = self.request.query_params.get('tag')
        if tag:
            qs = qs.filter(tags__slug=tag)
        is_featured = self.request.query_params.get('is_featured')
        if is_featured is not None:
            qs = qs.filter(is_featured=is_featured.lower() == 'true')
        return qs.distinct()

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        if not request.user.is_authenticated or not request.user.is_superuser:
            if post.status != 'PUBLISHED':
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        visitor_id = request.headers.get('X-Visitor-Id')
        if visitor_id:
            key = f'viewed_post_{post.id}_{visitor_id}'
            if not request.session.get(key):
                Post.objects.filter(pk=post.id).update(views_count=F('views_count') + 1)
                request.session[key] = True
        serializer = self.get_serializer(Post.objects.get(pk=post.id), context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='like')
    @throttle_classes([LikeToggleThrottle])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        visitor_id = request.headers.get('X-Visitor-Id')
        if not visitor_id:
            return Response({'detail': 'X-Visitor-Id header is required.'}, status=status.HTTP_400_BAD_REQUEST)
        like = PostLike.objects.filter(post=post, visitor_id=visitor_id).first()
        if like:
            like.delete()
            liked = False
        else:
            PostLike.objects.create(post=post, visitor_id=visitor_id, ip_address=request.META.get('REMOTE_ADDR'))
            liked = True
        return Response({'liked': liked, 'likes_count': post.likes.count()})

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    @throttle_classes([CommentCreateThrottle])
    def comments(self, request, *args, **kwargs):
        post = self.get_object()
        if request.method == 'GET':
            queryset = post.comments.filter(is_approved=True).select_related('parent').order_by('-created_at')
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)
        serializer = CommentSerializer(data={
            'post': post.id,
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'website': request.data.get('website'),
            'content': request.data.get('content'),
            'parent': request.data.get('parent') or None,
        })
        if serializer.is_valid():
            comment = serializer.save(post=post)
            comment.is_approved = False
            comment.save(update_fields=['is_approved'])
            return Response({'message': 'Your comment is awaiting approval.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('post').all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CommentPagination
    filterset_fields = ['is_approved', 'post']


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = ContactPagination
    filterset_fields = ['is_read']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return self.queryset
        return ContactMessage.objects.none()

    @throttle_classes([ContactCreateThrottle])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([AnonymousRateThrottle])
def dashboard_stats(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return Response({'detail': 'Owner access required.'}, status=403)
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='PUBLISHED').count()
    draft_posts = Post.objects.filter(status='DRAFT').count()
    total_projects = Project.objects.count()
    total_skills = Skill.objects.count()
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    total_likes = PostLike.objects.count()
    total_views = Post.objects.aggregate(total=Sum('views_count'))['total'] or 0
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    top_posts = list(Post.objects.filter(status='PUBLISHED').annotate(likes=Count('likes')).order_by('-views_count')[:5].values('title', 'slug', 'views_count', 'likes'))
    recent_comments = list(Comment.objects.order_by('-created_at')[:5].values('id', 'name', 'content', 'post__title', 'created_at'))
    return Response({
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_projects': total_projects,
        'total_skills': total_skills,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
        'total_likes': total_likes,
        'total_views': total_views,
        'unread_messages': unread_messages,
        'top_posts': top_posts,
        'recent_comments': recent_comments,
        'posts_per_month': [],
    })
