from django.contrib.auth.decorators import user_passes_test


def company_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.role == 'company',
        login_url="accounts:login"
    )(view_func)
    return decorated_view_func

