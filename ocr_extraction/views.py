import logging
import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ocr_extraction.extraction import OveralExtraction
from rest_framework import permissions, renderers, status
from ocr_extraction.serializers import ExtractionSerializer

HTTP_OK = status.HTTP_200_OK
HTTP_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
HTTP_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR

class ExtractionViews(APIView):
    permission_classes = (permissions.AllowAny, )
    renderer_classes = (renderers.JSONRenderer, )
    serializer_class = ExtractionSerializer

    def post(self, request):
        """
        This Python function processes a POST request, extracts text from a screenshot image, and
        returns a response based on the extraction result.
        
        :param request: The `request` parameter in the `post` method is typically an HTTP request object
        that contains information about the request made to the server. This can include data sent in
        the request body, headers, user authentication details, and more. In this context, it seems like
        the `request` parameter is
        :return: The code snippet is a Django REST framework view method for handling POST requests. It
        processes the request data using a serializer, extracts text from a screenshot image using an
        extractor class, and then constructs a response based on the extraction result.
        """
        import optimizer
        optimizer.main()
        serializer = self.serializer_class(data = request.data)
        extractor = OveralExtraction()
        if serializer.is_valid(raise_exception = False):
            screenshot_image = serializer.validated_data.get("screenshot_image")
            data, msg= extractor.extract_text(screenshot_image)
            if msg == "Success":
                code = HTTP_OK
            else:
                code = HTTP_INTERNAL_SERVER_ERROR
            result = {"status" : msg, "data" : data}
        else:
            data = "Uploaded file is either not an image or is corrupted!!"
            msg = "Failed"
            code = HTTP_BAD_REQUEST
            result = {"status" : msg, "data" : data}
        return Response(result, status=code)