from django.db import models
from .coremodels import BaseTimestampedModel, BaseUserTrackedModel
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, List, Optional, Union
from django.core.paginator import Paginator


class EnableStatusModelMixin(models.Model):
    choice = [("ENABLE", "Enable"), ("DISABLE", "Disable")]

    enable_status = models.CharField(
        choices=choice, verbose_name="Enable Status", max_length=7, default="ENABLE")

    class Meta:
        abstract = True


class CityModelMixin(models.Model):
    """
    Mixin which can be used to store city details
    """
    city_choices = [("AUH", "Abu Dhabi"), ("DXB", "Dubai"), ("SHJ", "Sharjah"), ("AJM",
                                                                                 "Ajman"), ("UAQ", "Umm Al Quwain"), ("RAK", "Ras Al Khaimah"), ("FUJ", "Fujairah")]

    city = models.CharField(choices=city_choices,
                            verbose_name="City", max_length=255, default="DXB")

    class Meta:
        abstract = True


class AuditModelMixin(BaseTimestampedModel, BaseUserTrackedModel):
    """
    Mixin which will helps in logging user activity for audit
    """
    class Meta:
        abstract = True


class ExceptionMixin:
    """
    Mixin which will capture any exception and return response with the error message
    """

    def handle_exception(self, exc):
        data = {
            "status": "Failed",
            "message": exc.args
        }
        resp_status = status.HTTP_200_OK
        if hasattr(exc, "status_code"):
            if exc.status_code == 401:
                data["message"] = "Invalid Authentication Credentials"
                resp_status = status.HTTP_401_UNAUTHORIZED
            if exc.status_code == 405:
                data["message"] = f"{exc.args[0]} Method not Allowed"
                resp_status = status.HTTP_405_METHOD_NOT_ALLOWED
            if exc.status_code == 400:
                data["message"] = "Bad Request"
                resp_status = status.HTTP_400_BAD_REQUEST
        else:
            data["message"] = exc.args
            resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(data, status=resp_status)


class CustomResponseMixin:
    """
    Mixin which consists of methods which can be used to send a customized response
    """

    def custom_response(self, message: Optional[str] = None, data: Optional[Union[list, dict]] = None, success: bool = True, resp_status: Optional[str] = None, headers: Optional[dict] = None, page_number: int = None) -> Response:
        """
        Method which will act as a general template for the responses that needs to be sent out

        :param message: Message that needs to be included in the response
        :type message: str, optional

        :param data: Data that needs to be included in the response
        :type message: list, dict, optional

        :param status: Object which contains the status code for the response
        :type status: class:`restframework.status`

        :param success: Notifies if response is a success response or failure response
        :type success: boolean

        :param headers: Headers to be passed to the response
        :type headers: dict, optional 

        :param page_number: Page number of the data that needs to be displayed
        :type page_number: int, optional 

        :return: Response message for a request
        :rtype: class:`restframework.response.Response`

        """
        resp_status = status.HTTP_200_OK if not resp_status else resp_status
        resp_data = {
            "status": "Success" if success else "Failed"
        }
        if message:
            resp_data["message"] = message

        if data or data == []:
            if page_number:
                paginate = Paginator(data, 12)
                paginate_data = paginate.get_page(page_number)
                resp_data["data"] = paginate_data.object_list
                resp_data["num_pages"] = paginate.num_pages
            else:
                resp_data["data"] = data

        return Response(resp_data, status=resp_status, headers=headers)
