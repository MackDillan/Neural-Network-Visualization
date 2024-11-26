import uuid
import json
from datetime import datetime, timezone
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db import collection_project as mongo_projects

def serialize_document(doc):
    """
    Convert MongoDB document fields to JSON serializable formats.
    """
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc


class ProjectView(APIView):
    """API View for managing models stored in MongoDB."""

    def get(self, request, pk=None):
        """
        Retrieve documents.
        - If `pk` is provided, returns a specific document with its details.
        - If `pk` is not provided, returns a list of documents.
        """
        if pk:
            print(pk)
            print(list(mongo_projects.find({"_id": pk})))
            result = list(mongo_projects.find(
                {"_id": pk}, 
                {"_id": 1, "name": 1, "model_link": 1, "dataset_name": 1, 
                "description": 1, "created": 1, "updated": 1}
            ))
            if not result:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
            result = [serialize_document(doc) for doc in result]
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = list(mongo_projects.aggregate([
                {"$sort": {"updated": -1}},
                {"$group": {
                    "_id": "$_id",
                    "name": {"$first": "$name"},
                    "model_link": {"$first": "$model_link"},
                    "dataset_name": {"$first": "$dataset_name"},
                    "description": {"$first": "$description"},
                    "updated": {"$first": "$updated"}
                }}
            ]))
            result = [serialize_document(doc) for doc in result]
            return Response(result, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Create a new document.
        - Expects a JSON payload in the request body containing:
        `name`, `model_uid`, `dataset_name`, `description`.
        - Generates a new document ID and adds `created` and `updated` timestamps.
        """
        if not request.body:
            return Response({"error": "No JSON string provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = json.loads(request.body)

            if not all(key in data for key in ["name", "model_uid", "dataset_name", "description"]):
                return Response({"error": "Missing required fields: 'name', 'model_uid', 'dataset_name', 'description'"},
                                status=status.HTTP_400_BAD_REQUEST)

            doc_id = str(uuid.uuid4())

            now = datetime.now(timezone.utc).isoformat()
            model = {
                "_id": doc_id,
                "name": data["name"],
                "model_uid": data["model_uid"],
                "dataset_name": data["dataset_name"],
                "description": data["description"],
                "created": now,
                "updated": now
            }

            mongo_projects.insert_one(model)
            return Response({"message": "Document created successfully", "id": doc_id}, status=status.HTTP_201_CREATED)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON string"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, pk):
        """
        Update an existing document.
        - Expects a JSON payload in the request body containing:
        `name`, `model_uid`, `dataset_name`, `description`.
        - Updates the fields provided in the payload, retaining the old values for missing keys.
        - Updates the `updated` timestamp.
        """
        if not request.body:
            return Response({"error": "No JSON string provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = json.loads(request.body)

            existing_doc = mongo_projects.find_one({"_id": pk})
            if not existing_doc:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

            updated_doc = {
                "name": data.get("name", existing_doc["name"]),
                "model_uid": data.get("model_uid", existing_doc["model_uid"]),
                "dataset_name": data.get("dataset_name", existing_doc["dataset_name"]),
                "description": data.get("description", existing_doc["description"]),
                "updated": datetime.now(timezone.utc).isoformat()
            }

            mongo_projects.update_one({"_id": pk}, {"$set": updated_doc})
            return Response({"message": "Document updated", "id": pk}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON string"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, pk):
        """
        Delete a document by its ID (`pk`).
        - Deletes the document with the specified `id`.
        """
        result = mongo_projects.delete_one({"_id": pk})
        if result.deleted_count > 0:
            return Response({"message": "Document deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
