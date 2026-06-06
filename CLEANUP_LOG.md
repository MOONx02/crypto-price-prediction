# Cleanup Log

## 2026-05-02 - Repository declutter for EC execution

Objective: reduce notebook/version confusion before implementing extra credit extensions.

### Actions taken
- Created canonical execution notebook: `notebooks/Crypto_Colab_EC_v1.ipynb` (copied from `notebooks/Crypto_Colab_AllInOne_v9.ipynb` baseline).
- Archived root-level duplicate/result notebooks to `archive/legacy_artifacts/root_notebook_exports/` (kept, not deleted):
  - `Crypto_Colab_AllInOne_v7_results.ipynb`
  - `Crypto_Colab_AllInOne_v9.ipynb`
  - `Crypto_Colab_AllInOne_v9.5.ipynb`
  - `Crypto_Colab_AllInOne_v9_5results.ipynb`
  - `nvdaresults.ipynb`
  - `result1.ipynb`
  - `resut2.ipynb`
  - `v8_results.ipynb`
  - `v8_stocks_results.ipynb`

### Result
- Main workflow location is now `notebooks/`.
- EC development starts from `notebooks/Crypto_Colab_EC_v1.ipynb`.
- Historical exports are preserved in a dedicated archive path.

## 2026-05-02 - Non-related scratch files removed

Objective: remove root-level non-project artifacts that may cause confusion.

### Actions taken
- Permanently deleted approved scratch files:
  - `hi.html`
  - `script.docx`
  - `updated.pdf`

### Result
- Root directory has fewer unrelated artifacts.
- Deletions were limited to explicitly user-approved files.

## 2026-05-02 - Consolidated documents and presentations

Objective: move report/proposal/presentation artifacts out of project root and remove duplicate copies.

### Actions taken
- Created archive folder structure:
  - `archive/documents_presentations/root/`
  - `archive/documents_presentations/Submision/`
- Moved all `.docx`, `.pdf`, and `.pptx` files from root and `Submision/` into that folder structure.
- Ran duplicate cleanup using SHA-256 content hashes across all moved document/presentation files.

### Result
- Documents and presentation files are consolidated under `archive/documents_presentations/`.
- Duplicate scan result: `checked=16`, `unique=16`, `deleted=0` (no exact-content duplicates found).
