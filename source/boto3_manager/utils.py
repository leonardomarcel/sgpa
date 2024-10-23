from django.conf import settings
from django.db import connection
from boto3_manager.session import AsAwsUtil
from typing import IO, Dict

class S3Bucket(AsAwsUtil):
    SCHEMA_URI_START = 's3://'
    RESOURCE = 's3'
    ATTRNAME = 's3_utils'

    def __init__(self, app_: str, view_: str):
        super().__init__(S3Bucket.RESOURCE, app_, view_)

    def s3_put_temporary_file(self, obj_name: str, body: str):
        return self.client.put_object(
            ACL='private',
            Body=body,
            Bucket=settings.TENANT_S3_STORAGE,
            Key=self._get_default_temp_storage_key(obj_name)
        )

    def s3_delete_temporary_file(self, obj_name: str):
        return self.client.delete_object(
            Bucket=settings.TENANT_S3_STORAGE,
            Key=self._get_default_temp_storage_key(obj_name)
        )

    def put(self, *args, **kwargs):
        """
            Call s3.put_object without default Bucket and default Key.
        """
        return self.client.put_object(*args, **kwargs)

    def s3_put_from_view(self, obj_name: str, body: str):
        return self.client.put_object(
            ACL='private',
            Body=body,
            Bucket=settings.TENANT_S3_STORAGE,
            Key=self._get_default_key(obj_name)
        )

    def s3_get_uri_path(self, obj_name: str):
        return self._get_default_key(obj_name)
    

    def s3_get_from_view(self, obj_name: str):
        return self.client.get_object(
            Bucket=settings.TENANT_S3_STORAGE,
            Key=self._get_default_key(obj_name)
        )

    def s3_del_from_view(self, obj_name: str, is_full_uri=False):
        return self.client.delete_object(
            Bucket=settings.TENANT_S3_STORAGE,
            Key=self._get_default_key(obj_name) if not is_full_uri else obj_name
        )

    def get(self, *args, **kwargs):
        """
            Call s3.get_object without default Bucket and default Key.
        """
        return self.client.get_object(*args, **kwargs)

    def s3_upload_fileobj_from_view(self, obj_name: str, obj_stream: IO):
        return self.client.upload_fileobj(
            Fileobj=obj_stream,
            Bucket=settings.TENANT_S3_STORAGE,
            Key=self._get_default_key(obj_name),
        )
    
    def s3_upload_fileobj(self, obj_name: str, obj_stream: IO):
        return self.client.upload_fileobj(
            Fileobj=obj_stream,
            Bucket=settings.TENANT_S3_STORAGE,
            Key=self._get_default_temp_storage_key(obj_name),
        )

    def del_object(self, obj_name: str):
        return self.client.delete_objects(
            Bucket=settings.TENANT_S3_STORAGE,
            Key=self._get_default_key(obj_name)
        )
    
    def del_objects(self, prefix: str):
        return self.client.delete_objects(
            Bucket=settings.TENANT_S3_STORAGE,
            Delete={'Objects': self._get_objects(settings.TENANT_S3_STORAGE, prefix)}
        )

    def del_direct(self, *args, **kwargs):
        """
            CAll s3.del_object direct without default Bucket and default Key.
        """
        return self.client.delete_object(*args, **kwargs)

    @property
    def _schema(self):
        return connection.schema_name

    def _get_default_key(self, obj_name: str):
        # PATH FOR APP AND VIEW
        # Ex: s3://<default_tenants_storage>/<tenant_id>/<app>/<view>/temp_file.foo
        return f'{self._schema}/{self.app}/{self.view}/{obj_name}'
    
    def _get_objects(self, bucket_name: str, prefix: str):
        response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        return [{'Key': obj['Key']} for obj in response['Contents']]
    
    def _get_default_temp_storage_key(self, obj_name: str):
        # PATH FOR TENANT TEMP FILES
        return f'{self._schema}/{settings.TENANT_S3_STORAGE_TEMP[1:]}/{obj_name}'

    def is_object_in_bucket(self, bucket_name: str, bucket_obj_name_or_path: str) -> bool:
        pass


__all__ = ['SQS', 'S3Bucket', 'ECSUtil']