#!/usr/bin/env python
"""
Read icon slugs from icons.txt, fetch their JSON metadata from Lucide's GitHub,
extract tags, embed with all-MiniLM-L6-v2, and store into Redis as a vector index.

Requirements:
    pip install sentence-transformers redisvl python-dotenv requests
Env vars:
    REDIS_URL          # e.g. redis://:password@localhost:6379/0
    ICONS_FILE_PATH    # optional, default: ./icons.txt
"""

import json
import os
from typing import List

import numpy as np
import requests
import redis
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from redisvl.index import SearchIndex

from config import (
    INDEX_NAME,
    KEY_PREFIX,
    EMBEDDING_MODEL_NAME,
    EMBEDDING_DIM,
    LUCIDE_RAW_BASE,
    TEST_SENTENCES
)

# ----------------- Config -----------------

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")  # e.g. redis://default:password@localhost:6379/0
ICONS_FILE_PATH = os.getenv("ICONS_FILE_PATH", "icons.txt")


# ----------------- Helpers -----------------

def read_icon_slugs(path: str) -> List[str]:
    """
    Read icon slugs from a text file, one per line.
    Ignores blank lines and lines starting with '#'.
    Example of icons.txt:
        a-arrow-down
        alert-triangle
        check-circle-2
    """
    slugs: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw:
                continue
            if raw.startswith("#"):
                continue
            slugs.append(raw)
    return slugs


def slug_to_component_name(slug: str) -> str:
    """
    Convert a slug like 'a-arrow-down' -> 'AArrowDown'
    which matches lucide-react's component naming convention.
    """
    parts = slug.split("-")
    return "".join(p.capitalize() for p in parts if p)


def fetch_icon_metadata(slug: str) -> dict:
    """
    Fetch the Lucide icon JSON from GitHub raw content.
    Expects a structure that includes "tags" and possibly other metadata.
    URL pattern:
        https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/{slug}.json
    """
    url = f"{LUCIDE_RAW_BASE}{slug}.json"
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch metadata for '{slug}' "
            f"(status {resp.status_code}) from {url}"
        )
    return resp.json()


def build_description(name: str, slug: str, tags: List[str]) -> str:
    """
    Build a semantically rich description string to embed.

    We put tags and (if present) categories in the text so the embedding
    captures those semantics, but we only *store* tags in Redis.
    """
    tag_str = ", ".join(tags) if tags else "icon"

    base = (
        f"{name} - {slug}; {tag_str}"
    )

    return base

def create_index_if_needed(r: redis.Redis) -> SearchIndex:
    """
    Create the Redis vector index if it doesn't exist yet.
    Stored fields:
        - name: text
        - slug: text
        - tags: text (JSON array as string)
        - embedding: vector (cosine)
    """
    index_config = {
        "index": {
            "name": INDEX_NAME,
            "prefix": KEY_PREFIX,
            "storage_type": "hash",
        },
        "fields": [
            {"name": "name", "type": "text"},
            {"name": "slug", "type": "text"},
            {"name": "tags", "type": "text"},  # JSON-encoded array string
            {
                "name": "embedding",
                "type": "vector",
                "attrs": {
                    "dims": EMBEDDING_DIM,
                    "algorithm": "flat",
                    "distance_metric": "cosine",
                },
            },
        ],
    }

    # Build the index object from config
    index = SearchIndex.from_dict(index_config)

    # Attach the redis client to the index (important with newer redisvl)
    index.set_client(r)

    # Now exists() takes no arguments
    if not index.exists():
        print(f"Creating index '{INDEX_NAME}'...")
        index.create()
    else:
        print(f"Index '{INDEX_NAME}' already exists, using existing one.")

    return index

# ----------------- Main -----------------

def main():
    if not REDIS_URL:
        raise RuntimeError("REDIS_URL env var is required")

    print(f"Reading icon slugs from {ICONS_FILE_PATH}...")
    slugs = read_icon_slugs(ICONS_FILE_PATH)
    if not slugs:
        print("No icon slugs found in icons.txt; nothing to do.")
        return

    print(f"Loaded {len(slugs)} icon slugs.")

    print("Connecting to Redis...")
    r = redis.from_url(REDIS_URL)

    # Clean existing lucide:* keys from Redis
    print("Cleaning existing lucide:* keys from Redis...")
    try:
        keys = r.keys("lucide:*")
        if keys:
            r.delete(*keys)
            print(f"Deleted {len(keys)} existing keys.")
        else:
            print("No existing keys to delete.")
    except Exception as e:
        print(f"Error cleaning Redis keys: {e}")

    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    index = create_index_if_needed(r)

    docs = []

    for slug in slugs:
        component_name = slug_to_component_name(slug)

        print(f"Processing icon '{slug}' ({component_name})...")

        # Fetch metadata JSON from GitHub
        meta = fetch_icon_metadata(slug)

        # Lucide JSON is expected to contain "tags"
        tags: List[str] = meta.get("tags", [])
        if not isinstance(tags, list):
            # normalize if it's something weird
            tags = list(tags) if tags else []

        description = build_description(component_name, slug, tags)

        # Compute embedding
        embedding_vector: List[float] = model.encode(description).tolist()
        if len(embedding_vector) != EMBEDDING_DIM:
            raise ValueError(
                f"Embedding dimension mismatch for {slug}: "
                f"expected {EMBEDDING_DIM}, got {len(embedding_vector)}"
            )

        # Convert to float32 bytes for Redis hash storage
        embedding_bytes = np.array(embedding_vector, dtype=np.float32).tobytes()

        doc = {
            "name": slug,
            "description": description,
            "embedding": embedding_bytes,  # <-- bytes, not list
        }

        docs.append(doc)

    if docs:
        print(f"Indexing {len(docs)} icons into Redis...")
        index.load(docs)
        print("Done indexing Lucide icons.")
    else:
        print("No icons to index.")

    # Test the index with sample sentences
    print("\n" + "="*60)
    print("Testing vector search with sample sentences...")
    print("="*60 + "\n")

    for i, sentence in enumerate(TEST_SENTENCES, 1):
        # Encode the test sentence (suppress progress bar)
        query_embedding = model.encode(sentence, show_progress_bar=False).tolist()
        query_bytes = np.array(query_embedding, dtype=np.float32).tobytes()

        # Perform vector search (top 1 result)
        from redisvl.query import VectorQuery

        query = VectorQuery(
            vector=query_bytes,
            vector_field_name="embedding",
            return_fields=["name", "description"],
            num_results=1
        )

        results = index.query(query)

        if results:
            top_icon = results[0].get("name", "N/A")
            print(f"[Test {i}] \"{sentence}\" => {top_icon}")
        else:
            print(f"[Test {i}] \"{sentence}\" => No results found")

    print("\n" + "="*60)
    print("Testing complete!")
    print("="*60)


if __name__ == "__main__":
    main()