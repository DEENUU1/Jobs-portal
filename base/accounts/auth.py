from django.contrib.auth.decorators import user_passes_test


def company_required(view_func):
    """
    This function is a decorator that requires a user to have the role of 'company' to access a particular view.
    Parameters:
        view_func (function): The original view function that requires a 'company' role to access.
    Returns:
        decorated_view_func (function): A new function that wraps the original view function and checks
        if the user has the required role before calling the original view function.
        If the user does not have the required role, they are redirected to the login page specified in the decorator.
    """
    decorated_view_func = user_passes_test(
        lambda user: user.role == "company", login_url="accounts:login"
    )(view_func)
    return decorated_view_func


def user_required(view_func):
    """
    This function is a decorator that requires a user to have the role of 'user' to access a particular view.
    Parameters:
        view_func (function): The original view function that requires a 'user' role to access.
    Returns:
        decorated_view_func (function): A new function that wraps the original view function and checks
        if the user has the required role before calling the original view function.
        If the user does not have the required role, they are redirected to the login page specified in the decorator.
    """
    decorated_view_func = user_passes_test(
        lambda user: user.role == "user", login_url="accounts:login"
    )(view_func)
    return decorated_view_func
