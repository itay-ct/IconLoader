"""
Configuration file for IconLoader
Customize these values as needed for your use case.
"""

# Redis Index Configuration
INDEX_NAME = "lucide_icon_index"
KEY_PREFIX = "lucide:icon:"

# Embedding Model Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Lucide GitHub Repository
LUCIDE_RAW_BASE = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/"

# Test sentences for validating the vector search
TEST_SENTENCES = [
    "Found 5 places offering a relaxing drink for your tour.",
    "I found 9 parks to enjoy nature's beauty nearby.",
    "There are 3 locations of cultural interest, ready to inspire.",
    "Found 8 exciting sports and activity locations around.",
    "Found 17 delicious food spots awaiting your hungry stomach.",
    "Discovered 4 historical landmarks worth visiting.",
    "Located 6 shopping centers for your retail therapy.",
    "Found 12 entertainment venues for a fun night out.",
    "There are 7 hotels offering comfortable accommodation.",
    "Spotted 10 scenic viewpoints for amazing photos."
]

