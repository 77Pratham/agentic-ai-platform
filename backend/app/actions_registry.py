import os
import time

# --- ACTION IMPLEMENTATIONS ---

def retrieve_documents(params: dict):
    """
    Simulate document retrieval.
    Later this will connect to RAG ingestion.
    """
    time.sleep(1)
    docs = ["doc1.txt", "doc2.txt"]
    return {
        "documents": docs,
        "count": len(docs)
    }

def generate_report(params: dict):
    """
    Generate a dummy report file.
    """
    time.sleep(1)

    filename = "report.txt"
    with open(filename, "w") as f:
        f.write("This is a generated report.\n")

    return {
        "file": filename
    }

def send_email(params: dict):
    """
    Dry-run email sender.
    """
    time.sleep(1)
    return {
        "status": "sent",
        "mode": params.get("mode", "dry_run")
    }

def clarify_intent(params: dict):
    return {
        "question": params.get("question")
    }

# --- ACTION REGISTRY ---

ACTION_REGISTRY = {
    "retrieve_documents": retrieve_documents,
    "generate_report": generate_report,
    "send_email": send_email,
    "clarify_intent": clarify_intent
}
