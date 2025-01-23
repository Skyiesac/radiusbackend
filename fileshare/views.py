from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FileUploaded
from .serializers import FileUploadedSerializer


# Create your views here.
class FileUploadView(APIView):
    serializer_class = FileUploadedSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = self.serializer_class(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(
                {
                    "status": True,
                    "access_code": file_serializer.data["access_code"],
                    "message": "File Uploaded successfully!",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": False, "error": file_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class FileAccessView(APIView):
    serializer_class = FileUploadedSerializer

    def get(self, request, file_id, access_code):
        try:
            file = FileUploaded.objects.get(id=file_id, access_code=access_code)
        except FileUploaded.DoesNotExist:
            return Response(
                {"status": False, "message": "File not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(file)
        return Response(
            {"status": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, file_id, access_code):
        try:
            file = FileUploaded.objects.get(id=file_id, access_code=access_code)
        except FileUploaded.DoesNotExist:
            return Response(
                {"status": False, "message": "File not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        file.delete()
        return Response(
            {"status": True, "message": "File deleted successfully!"},
            status=status.HTTP_200_OK,
        )
