"""Delete ALL documents in the feedback collection (development/test data only).

Run from the backend folder:  python -m scripts.reset_feedback --yes
"""

import sys

from app.database import get_feedback_collection


def main() -> None:
    if "--yes" not in sys.argv:
        sys.exit("This deletes every feedback document. Re-run with --yes to confirm.")
    deleted = 0
    for doc in get_feedback_collection().stream():
        doc.reference.delete()
        deleted += 1
    print(f"Deleted {deleted} document(s)")


if __name__ == "__main__":
    main()
