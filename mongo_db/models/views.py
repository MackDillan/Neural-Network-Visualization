import datetime
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
import json
from .db import documents


class ModelsView(APIView):
    def get(self, request, pk=None):
        if pk:
            # Retrieve all versions of the document by GUID
            result = list(documents.find({"_id": pk}, {"_id": 1, "version": 1, "json_data": 1, "created": 1, "updated": 1}))
            if not result:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(result, status=status.HTTP_200_OK)
        else:
            # Retrieve the latest version of all documents
            result = list(documents.aggregate([
                {"$sort": {"version": -1}},
                {"$group": {"_id": "$_id", "latest_version": {"$first": "$version"}, "updated": {"$first": "$updated"}}}
            ]))
            return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        # Check if JSON data is provided in the request body
        if not request.body:
            return Response({"error": "No JSON string provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parse JSON content from the request body
            json_content = json.loads(request.body)

            # Generate GUID for the document
            doc_id = str(uuid.uuid4())

            # Insert the first version of the document
            now = datetime.datetime.utcnow()
            document = {
                "_id": doc_id,
                "version": 1,
                "json_data": json_content,
                "created": now,
                "updated": now
            }

            # Save the document to MongoDB
            documents.insert_one(document)
            return Response({"message": "JSON uploaded successfully", "id": doc_id, "version": 1}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON string"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        # Ensure JSON string is provided in the request body
        if not request.body:
            return Response({"error": "No JSON string provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parse JSON content from the request body
            json_content = json.loads(request.body)

            # Find the latest version of the document
            last_doc = documents.find_one({"_id": pk}, sort=[("version", -1)])
            if not last_doc:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

            now = datetime.datetime.utcnow()
            new_version = last_doc["version"] + 1
            document = {
                "version": new_version,
                "json_data": json_content,
                "created": last_doc["created"],
                "updated": now
            }

            # Обновляем документ с использованием update_one
            documents.update_one({"_id": pk}, {"$set": document})
            return Response({"message": "Document updated", "id": pk, "version": new_version}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON string"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, pk):
        # Delete all versions of the document by GUID
        result = documents.delete_many({"_id": pk})
        if result.deleted_count > 0:
            return Response({"message": f"{result.deleted_count} versions deleted"}, status=status.HTTP_200_OK)
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)


class JSONDataDownloadView(APIView):
    def get(self, request, pk):
        try:
            # Find the document by ID
            document = documents.find_one({"_id": pk})
            if not document:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

            # Extract the JSON data field
            json_data = document.get("json_data")
            if not json_data:
                return Response({"error": "No JSON data in the document"}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the JSON data into a string
            json_string = json.dumps(json_data, indent=4)

            # Return the JSON string directly in the response
            return Response({"json_data": json_string}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
