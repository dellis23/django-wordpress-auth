from django.http import HttpResponse

from wordpress_auth.decorators import (
    wordpress_login_required, wordpress_requires_role,
    wordpress_requires_capability
)


@wordpress_login_required
def show_session(request):
    return HttpResponse(request.wordpress_user.login)


@wordpress_requires_role('lima_member')
def test_roles(request):
    return HttpResponse('Success')


@wordpress_requires_capability('view_cls_records')
def test_capabilities(request):
    return HttpResponse('Success')
