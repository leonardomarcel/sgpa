from boto3_manager.utils import __all__ # noqa
from boto3_manager.session import AsAwsUtil
from typing import Type, Callable, List

import boto3_manager.utils as boto3mod_utils

# Preload the classes
boto3_utils: List[Type[AsAwsUtil]] = []
for boto3_util in __all__:
    Boto3Util: Type[AsAwsUtil] = getattr(boto3mod_utils, boto3_util)
    if not hasattr(Boto3Util, 'ATTRNAME'):
        raise AttributeError(f'Class {Boto3Util.__class__} missing mandatory attribute ATTRNAME')
    boto3_utils.append(Boto3Util)


class Boto3UtilsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func: Callable, _, __):
        # Inject Boto3 Utils into request object
        for Boto3UtilClass in boto3_utils:
            view_name = view_func.__name__
            view_module = view_func.__module__ # noqa
            setattr(request, Boto3UtilClass.ATTRNAME, Boto3UtilClass(view_module, view_name)) # noqa
        return None