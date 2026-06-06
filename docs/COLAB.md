# Running on Google Colab

Use Colab for faster CPU/GPU and to run the notebooks in the cloud. Data can be re-downloaded each session or saved to Google Drive.

---

## If your repo is private

Colab can’t clone a private repo without authentication. Use one of these:

**Option A – GitHub Personal Access Token (recommended)**  
1. On GitHub: **Settings → Developer settings → Personal access tokens** (or [github.com/settings/tokens](https://github.com/settings/tokens)). Generate a token with `repo` scope.  
2. In Colab: open the **🔑 Secrets** panel in the left sidebar (key icon). Add a secret: name **`GITHUB_TOKEN`**, value = your token.  
3. Use **00_colab_setup.ipynb** as usual; the first cell will use this token to clone the private repo.

**Option B – Drive + ZIP (no token)**  
1. On your machine (or GitHub): download the repo as ZIP (e.g. **Code → Download ZIP** on the repo page, or `git archive`).  
2. Upload the ZIP to Google Drive (e.g. in a folder `crypto-price-prediction`).  
3. In a Colab notebook run once:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   !unzip -q "/content/drive/MyDrive/path/to/crypto-price-prediction-main.zip" -d /content
   %cd /content/crypto-price-prediction-main
   !pip install -q -r requirements.txt
   ```
   Then open `notebooks/01_data_and_baselines.ipynb` from the file browser. (Update the ZIP path to match your Drive.)

---

## Quick start (every new session)

In a **new Colab notebook**, run the two cells in **00_colab_setup.ipynb** (or the snippets below). The clone cell uses your **GITHUB_TOKEN** secret if the repo is private.

```python
# Cell 1: Clone (uses GITHUB_TOKEN from Colab Secrets if set, for private repos)
try:
  from google.colab import userdata
  token = userdata.get('GITHUB_TOKEN')
  repo = "https://" + token + "@github.com/MOONx02/crypto-price-prediction.git"
except Exception:
  repo = "https://github.com/MOONx02/crypto-price-prediction.git"
import subprocess
subprocess.run(["git", "clone", "-q", repo], check=True)
%cd crypto-price-prediction
```

```python
# Cell 2: Install dependencies
!pip install -q -r requirements.txt
```

Then:

- In the Colab **file browser** (left sidebar 📁), go to **crypto-price-prediction → notebooks** and open **01_data_and_baselines.ipynb** (or 02, 03). Run all cells.
- **Use the same runtime:** Run 00 first, then open 01 (or 02, 03) from the file browser *without* starting a new session. If you open 01 in a new “Open notebook” tab, the clone from 00 is still in that VM—notebooks 01–03 now detect Colab and use `/content/crypto-price-prediction` so `src` is found.

---

## Using the data

- **Each session:** The notebooks download data with `yfinance` and save to `data/` inside the clone. That folder lives only for the current runtime. When the session ends, it’s gone.
- **Re-use data next time:** Either re-run the download cells (fast, same data) or save to Google Drive (below).

### Optional: Save and load data from Google Drive

Run once to mount Drive and (optional) copy data there at the end of a run:

```python
from google.colab import drive
drive.mount('/content/drive')
# Optional: copy current data to Drive so next time you can skip download
# !cp -r data /content/drive/MyDrive/crypto-price-prediction-data
```

Next session, after cloning and `%cd crypto-price-prediction`, either re-download or restore from Drive:

```python
# Restore data from Drive (if you saved it)
!mkdir -p data
!cp -r /content/drive/MyDrive/crypto-price-prediction-data/* data/
```

Then run the rest of the notebook; it will use `data/BTC_USD_daily.parquet` etc. as usual.

---

## GPU (for LSTM in 03)

- **Runtime → Change runtime type → Toggle GPU** (T4 is free). The LSTM in **03_lstm.ipynb** will use GPU automatically if available.
- No code changes needed; TensorFlow picks up the GPU.

---

## Summary

| Step | Action |
|------|--------|
| 1 | New Colab notebook → run clone + `%cd crypto-price-prediction` + `pip install -r requirements.txt` |
| 2 | Open **notebooks/01_data_and_baselines.ipynb** (or 02, 03) from the file browser and run |
| 3 | Data is downloaded into `data/` in the clone; use it in 02 and 03 as-is |
| 4 | (Optional) Mount Drive and copy `data/` there to reuse in future sessions |
