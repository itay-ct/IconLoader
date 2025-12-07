# Setup Guide

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd IconLoader
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set your Redis URL:
   ```
   REDIS_URL=redis://default:your_password@your-redis-host.com:6379
   ```

5. **Run the script**
   ```bash
   python IconLoader.py
   ```

## Configuration

### Environment Variables (.env)
- `REDIS_URL` (required): Your Redis connection string
- `ICONS_FILE_PATH` (optional): Path to icons file (default: `icons.txt`)

### Application Settings (config.py)
- `INDEX_NAME`: Redis index name
- `KEY_PREFIX`: Prefix for Redis keys
- `EMBEDDING_MODEL_NAME`: Sentence transformer model to use
- `EMBEDDING_DIM`: Dimension of embeddings (384 for all-MiniLM-L6-v2)
- `LUCIDE_RAW_BASE`: Base URL for Lucide GitHub repository
- `TEST_SENTENCES`: List of test queries to validate the search

## Redis Setup

### Local Redis
```bash
# Install Redis (macOS)
brew install redis

# Start Redis
redis-server

# Use in .env
REDIS_URL=redis://localhost:6379
```

### Cloud Redis (Redis Cloud, AWS ElastiCache, etc.)
Get your connection URL from your provider and add it to `.env`

## Troubleshooting

### Model Download
On first run, the script will download the sentence-transformers model (~80MB). This is cached locally for future runs.

### Redis Connection Issues
- Verify your Redis URL is correct
- Check if Redis is running: `redis-cli ping` (should return PONG)
- Ensure firewall allows connection to Redis port

### Memory Issues
The embedding model requires ~500MB RAM. If running on limited resources, consider using a smaller model in `config.py`.

