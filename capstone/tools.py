"""
Moltbook tool stubs for the capstone.
"""

import os
from typing import Dict, Optional

import requests

MOLTBOOK_BASE_URL = "https://www.moltbook.com/api/v1"
MOLTBOOK_API_KEY = os.getenv("MOLTBOOK_API_KEY", "")


def _auth_headers() -> Dict[str, str]:
    if not MOLTBOOK_API_KEY:
        raise RuntimeError("Missing MOLTBOOK_API_KEY")
    return {
        "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
        "Content-Type": "application/json",
    }


def create_post(submolt: str, title: str, content: str) -> Dict:
    """
    Create a Moltbook post.
    Endpoint: POST /posts
    """
    url = f"{MOLTBOOK_BASE_URL}/posts"
    payload = {"submolt": submolt, "title": title, "content": content}
    resp = requests.post(url, json=payload, headers=_auth_headers(), timeout=20)
    resp.raise_for_status()
    return resp.json()


def add_comment(post_id: str, content: str, parent_id: Optional[str] = None) -> Dict:
    """
    Add a comment to a post.
    Endpoint: POST /posts/{post_id}/comments
    """
    url = f"{MOLTBOOK_BASE_URL}/posts/{post_id}/comments"
    payload = {"content": content}
    if parent_id:
        payload["parent_id"] = parent_id
    resp = requests.post(url, json=payload, headers=_auth_headers(), timeout=20)
    resp.raise_for_status()
    return resp.json()
