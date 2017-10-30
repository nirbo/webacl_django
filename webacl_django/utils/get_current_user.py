# -*- coding: utf-8 -*-
from contextlib import contextmanager
from threading import local

__author__ = 'Michal Kulaczkowski'

# thread local support
_thread_locals = local()


def set_current_user(user):
    """
    Assigns current user from request to thread_locals, used by
    CurrentUserMiddleware.
    """
    _thread_locals.user = user


def get_current_user():
    """
    Returns current user, or None.
    
    TODO: Move away from using this as a default value for db fields because
    then accessing obj.user results in another db query.
    """
    user = getattr(_thread_locals, 'user', None)
    return user


@contextmanager
def current_user(user):
    """
    Changes the current user just within a context.
    """
    old_user = get_current_user()
    set_current_user(user)
    yield
    set_current_user(old_user)

