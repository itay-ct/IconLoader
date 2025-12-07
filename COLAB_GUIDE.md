# Google Colab Guide for IconLoader

## Quick Start

### Option 1: Direct Link (Easiest)
1. Upload `IconLoader.ipynb` to your GitHub repository
2. Update the Colab badge link in the notebook with your GitHub username/repo
3. Click the "Open in Colab" badge to launch

### Option 2: Upload to Colab
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click **File → Upload notebook**
3. Upload `IconLoader.ipynb`
4. Run the cells in order

### Option 3: From GitHub
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click **File → Open notebook → GitHub**
3. Enter your repository URL
4. Select `IconLoader.ipynb`

## How to Use

### Step-by-Step Instructions

1. **Run Cell 1: Install Dependencies**
   - Installs all required Python packages
   - Takes ~30 seconds

2. **Run Cell 2: Configuration**
   - Enter your Redis URL when prompted (it won't be saved)
   - Format: `redis://default:password@host:6379`
   - The password input is hidden for security

3. **Run Cell 3: Icon List**
   - **Option A**: Upload your `icons.txt` file when prompted
   - **Option B**: Use the predefined icon list in the cell
   - You can edit the cell to add/remove icons

4. **Run Cell 4: Helper Functions**
   - Defines utility functions (no input needed)

5. **Run Cell 5: Connect to Redis**
   - Connects to your Redis instance
   - Cleans old data
   - Creates the vector index

6. **Run Cell 6: Load Model & Process Icons**
   - Downloads the embedding model (~80MB, first time only)
   - Fetches metadata for each icon from GitHub
   - Generates embeddings
   - Shows progress for each icon

7. **Run Cell 7: Index Icons**
   - Stores all icons in Redis
   - Quick operation

8. **Run Cell 8: Test Vector Search**
   - Runs 10 predefined test queries
   - Shows which icon matches each query

9. **Run Cell 9: Custom Search (Optional)**
   - Try your own search queries
   - Returns top 5 matching icons

## Key Differences from Python Script

### ✅ Advantages
- **No local setup required** - runs entirely in the cloud
- **Free GPU/TPU access** (though not needed for this project)
- **Easy sharing** - just share the notebook link
- **Interactive** - see results immediately after each step
- **File upload** - easy to upload `icons.txt` via UI
- **Secure credentials** - uses `getpass` so Redis URL isn't saved

### ⚠️ Considerations
- **Session timeout** - Colab sessions expire after ~12 hours of inactivity
- **Runtime disconnect** - Need to re-run all cells if disconnected
- **No persistent storage** - Model is re-downloaded each session (cached during session)
- **Network dependency** - Requires internet connection

## Tips & Tricks

### 1. Save Your Work
- **File → Save a copy in Drive** to save the notebook to your Google Drive
- Your Redis data persists (it's stored in Redis, not Colab)

### 2. Modify Icon List
Edit Cell 3 to change which icons to process:
```python
icon_slugs = [
    "beer", "wine", "coffee",  # Add your icons here
    "home", "user", "settings"
]
```

### 3. Change Test Queries
Edit the `TEST_SENTENCES` list in Cell 2 to test different queries

### 4. Adjust Search Results
In Cell 9, change `num_results=5` to get more/fewer results

### 5. Run All at Once
- **Runtime → Run all** to execute all cells sequentially
- You'll be prompted for Redis URL and icon file upload

### 6. Clear Output
- **Edit → Clear all outputs** to clean up the notebook before sharing

## Troubleshooting

### "Module not found" Error
- Re-run Cell 1 (Install Dependencies)
- Restart runtime: **Runtime → Restart runtime**

### Redis Connection Failed
- Check your Redis URL format
- Verify Redis is accessible from the internet
- Test with: `redis-cli -u YOUR_REDIS_URL ping`

### Icon Fetch Failed
- GitHub may rate-limit requests
- Add a small delay between icons (edit Cell 6)
- Use fewer icons for testing

### Model Download Slow
- First download takes ~1-2 minutes
- Subsequent runs in same session use cached model
- Colab has fast internet, usually quick

### Session Disconnected
- **Runtime → Reconnect**
- Re-run all cells (your Redis data is safe)

## Sharing Your Notebook

### Public Sharing
1. Upload to GitHub
2. Update the Colab badge URL in Cell 1:
   ```
   https://colab.research.google.com/github/YOUR_USERNAME/IconLoader/blob/main/IconLoader.ipynb
   ```
3. Share the GitHub link or Colab link

### Private Sharing
1. Save to Google Drive
2. Click **Share** button in Colab
3. Set permissions and share link

## Advanced: Mounting Google Drive

To save/load files from Google Drive, add this cell:

```python
from google.colab import drive
drive.mount('/content/drive')

# Then use paths like:
# '/content/drive/MyDrive/icons.txt'
```

## Performance Notes

- **Processing time**: ~1-2 seconds per icon
- **100 icons**: ~2-3 minutes total
- **Model loading**: ~30 seconds (first time)
- **Embedding generation**: Very fast with Colab's CPU

## Cost

- **Google Colab**: FREE (with usage limits)
- **Redis**: Depends on your provider
  - Redis Cloud: Free tier available
  - Local Redis: Free

## Next Steps

After running the notebook:
1. Your icons are indexed in Redis
2. You can query them from any application
3. The notebook can be re-run to update icons
4. Share the notebook with your team

## Need Help?

- Check the main README.md for project details
- See ISSUES_AND_RECOMMENDATIONS.md for known issues
- Open an issue on GitHub

