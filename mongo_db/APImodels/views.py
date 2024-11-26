import uuid
import json
from datetime import datetime, timezone
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db import collection_models as mongo_models


class ModelsView(APIView):
    """API View for managing models stored in MongoDB."""

    def get(self, request, pk=None):
        """
        Retrieve documents.
        - If `pk` is provided, returns a specific document with its details.
        - If `pk` is not provided, returns a list of documents with their latest versions and update timestamps.
        """
        if pk:
            result = list(mongo_models.find(
                {"_id": pk}, 
                {"_id": 1, "version": 1, "json_data": 1, "created": 1, "updated": 1}
            ))
            if not result:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = list(mongo_models.aggregate([
                {"$sort": {"version": -1}},
                {"$group": {
                    "_id": "$_id",
                    "latest_version": {"$first": "$version"},
                    "updated": {"$first": "$updated"},
                    "created": {"$first": "$updated"}
                }}
            ]))
            return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new document.
        - Expects a JSON payload in the request body.
        - Generates a new document ID and version number.
        - Stores the document along with creation and update timestamps.
        """
        if not request.body:
            return Response({"error": "No JSON string provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            json_content = json.loads(request.body)

            doc_id = str(uuid.uuid4())

            now = datetime.now(timezone.utc)
            model = {
                "_id": doc_id,
                "version": 1,
                "json_data": json_content,
                "created": now,
                "updated": now
            }

            mongo_models.insert_one(model)
            return Response({"message": "JSON uploaded successfully", "id": doc_id, "version": 1}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON string"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        """
        Update an existing document by creating a new version.
        - Expects a JSON payload in the request body.
        - Retrieves the latest version of the document using its ID (`pk`).
        - Creates a new version with updated data and a new timestamp.
        """
        if not request.body:
            return Response({"error": "No JSON string provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            json_content = json.loads(request.body)

            last_doc = mongo_models.find_one({"_id": pk}, sort=[("version", -1)])
            if not last_doc:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

            now = datetime.now(timezone.utc)
            new_version = last_doc["version"] + 1
            document = {
                "version": new_version,
                "json_data": json_content,
                "created": last_doc["created"],
                "updated": now
            }

            mongo_models.update_one({"_id": pk}, {"$set": document})
            return Response({"message": "Document updated", "id": pk, "version": new_version}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON string"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """
        Delete all versions of a document by its ID (`pk`).
        - Deletes all documents with the same ID (`_id`) regardless of version.
        """
        result = mongo_models.delete_many({"_id": pk})
        if result.deleted_count > 0:
            return Response({"message": f"{result.deleted_count} versions deleted"}, status=status.HTTP_200_OK)
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)


class ModelDownloadView(APIView):
    """API View for downloading JSON data from a document."""

    def get(self, request, pk):
        """
        Retrieve the JSON data of a specific document by its ID (`pk`).
        - Returns the `json_data` field of the document if it exists.
        """
        try:
            document = mongo_models.find_one({"_id": pk})
            if not document:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

            json_data = document.get("json_data")
            if not json_data:
                return Response({"error": "No JSON data in the document"}, status=status.HTTP_404_NOT_FOUND)

            json_string = json.dumps(json_data, indent=4)

            return Response({"json_data": json_string}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
