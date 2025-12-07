# Lucide Icon Loader

A Python tool that creates a searchable vector database of Lucide icons using semantic embeddings.

## Features

- Fetches icon metadata from the Lucide GitHub repository
- Generates semantic embeddings using the `all-MiniLM-L6-v2` model
- Stores icons in Redis with vector search capabilities
- Tests the index with sample queries to verify functionality

## Prerequisites

- Python 3.8+
- Redis instance (local or cloud-hosted)
- Internet connection (to fetch icon metadata and download the embedding model)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd IconLoader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Redis connection URL:
```
REDIS_URL=redis://default:your_password@your-redis-host.com:6379
```

## Usage

1. Add icon slugs to `icons.txt` (one per line)

2. Run the loader:
```bash
python IconLoader.py
```

The script will:
- Clean existing icon data from Redis
- Fetch metadata for each icon from Lucide's GitHub
- Generate embeddings and store them in Redis
- Run 10 test queries to verify the vector search

## Configuration

Edit the following constants in `IconLoader.py` if needed:

- `INDEX_NAME`: Redis index name (default: `lucide_icon_index`)
- `KEY_PREFIX`: Redis key prefix (default: `lucide:icon:`)
- `EMBEDDING_MODEL_NAME`: Sentence transformer model (default: `sentence-transformers/all-MiniLM-L6-v2`)

## How It Works

1. **Icon Loading**: Reads icon slugs from `icons.txt`
2. **Metadata Fetching**: Retrieves tags and categories from Lucide's GitHub repository
3. **Embedding Generation**: Creates semantic vectors using sentence transformers
4. **Redis Storage**: Stores icons with vector embeddings in Redis
5. **Testing**: Runs sample queries to verify search functionality

## Example Output

```
[Test 1] "Found 5 places offering a relaxing drink for your tour." => beer
[Test 2] "I found 9 parks to enjoy nature's beauty nearby." => trees
[Test 3] "There are 3 locations of cultural interest, ready to inspire." => building-2
```

## License

MIT

