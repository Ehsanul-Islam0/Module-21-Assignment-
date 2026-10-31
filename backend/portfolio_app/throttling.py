from rest_framework.throttling import ScopedRateThrottle


class AnonymousRateThrottle(ScopedRateThrottle):
    scope = 'anon'


class CommentCreateThrottle(ScopedRateThrottle):
    scope = 'comment_create'


class ContactCreateThrottle(ScopedRateThrottle):
    scope = 'contact_create'


class LikeToggleThrottle(ScopedRateThrottle):
    scope = 'like_toggle'
