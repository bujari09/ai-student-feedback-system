"""Analyze feedback left 'pending' or 'failed', e.g. after an NLP outage.

Run from the backend folder:  python -m scripts.reanalyze_pending
"""

from app.services.feedback_service import reanalyze_pending

if __name__ == "__main__":
    print(f"Re-analyzed {reanalyze_pending()} document(s)")
