from django.db import models


class BaseTimestampedModel(models.Model):
    """
    Abstract Model which stores timestamps of when the record was created and last updated
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseUserTrackedModel(models.Model):
    """
    Abstract Model which stores information of which user created and updated the record
    """
    created_by = models.ForeignKey('users.User', on_delete=models.SET(
        None), verbose_name="Posted By", related_name="create_user", null=True, blank=True)
    updated_by = models.ForeignKey('users.User', on_delete=models.SET(
        None), verbose_name="Updated By", related_name="update_user", null=True, blank=True)

    class Meta:
        abstract = True
