# Running on Google Colab

Use Colab for faster CPU/GPU and to run the notebooks in the cloud. Data can be re-downloaded each session or saved to Google Drive.

---

## Quick start (every new session)

In a **new Colab notebook**, run these two cells once:

```python
# Cell 1: Clone the repo and go to project root
!git clone https://github.com/MOONx02/crypto-price-prediction.git
%cd crypto-price-prediction
```

```python
# Cell 2: Install dependencies (Colab has many already; this adds yfinance, pyarrow, shap, etc.)
!pip install -q -r requirements.txt
```

Then either:

- **Option A:** In the Colab file browser (left sidebar), open **crypto-price-prediction → notebooks** and open **01_data_and_baselines.ipynb** (or 02, 03). Run all cells; the project’s `ROOT` logic will find the repo.
- **Option B:** Copy the contents of each notebook from GitHub into this Colab notebook and run. Keep the clone + pip cells at the top.

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
