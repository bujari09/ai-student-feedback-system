from functools import lru_cache

from google.cloud import firestore

from app.config import get_settings


@lru_cache
def get_firestore_client() -> firestore.Client:
    """Return a shared Firestore client.

    Credentials come from Application Default Credentials:
    - locally: `gcloud auth application-default login`
    - on the VM: the attached service account (metadata server)
    """
    settings = get_settings()
    return firestore.Client(project=settings.gcp_project_id, database=settings.firestore_database)


def get_feedback_collection() -> firestore.CollectionReference:
    return get_firestore_client().collection(get_settings().firestore_collection)
