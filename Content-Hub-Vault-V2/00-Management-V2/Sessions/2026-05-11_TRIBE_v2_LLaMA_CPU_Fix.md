---
date: 2026-05-11
type: session-log
status: handoff — ready to run
---

# TRIBE v2 — LLaMA CPU Offload Fix

## Goal
Fix persistent CUDA OOM blocking `analyze_content.py` from completing fMRI analysis on two vault files.

Continues: [[2026-05-11_TRIBE_v2_Analysis_VRAM_Debug]]

---

## Root Cause (Diagnosed This Session)

Previous fix (`batch_size=1`) was insufficient. The OOM error grew from 3.40 GiB → **9.70 GiB** because:

1. `device_map="auto"` places LLaMA layers greedily onto GPU first
2. With 4-bit LLaMA (~1.75 GB) + TRIBE (~700 MB) on GPU, only ~5.5 GB free
3. During the attention forward pass for each word-event (full document as context = ~1400 tokens), PyTorch tries to allocate the attention matrix on GPU
4. PyTorch reports "13.78 GiB allocated" = GPU + CPU combined; 0 bytes free on GPU
5. The 9.70 GiB contiguous allocation fails — no single contiguous block available

**Additional blocker caught before running**: 4-bit quantization (bitsandbytes) requires CUDA — it cannot run on CPU. Dropped entirely. Using fp16 on CPU instead (~6.4 GB RAM, fits in 15.7 GB).

**The fix**: `device_map={"": "cpu"} + torch_dtype=float16` — all LLaMA layers on CPU. TRIBE keeps GPU (~700 MB). Forward passes are slower but no OOM.

---

## Files Changed This Session

### `.venv-tribe\Lib\site-packages\neuralset\extractors\text.py`

**Patch 7a — `_load_model` (lines ~335–341)**: Replace entire `accelerate` try/except block:
```python
# Before (broken — 4-bit requires CUDA, can't run on CPU):
try:
    bnb_config = BitsAndBytesConfig(load_in_4bit=True, ...)
    kwargs = {"device_map": "auto", "quantization_config": bnb_config, ...}
except:
    kwargs = {"device_map": "auto", "torch_dtype": torch.float16, ...}

# After (fp16 on CPU, ~6.4 GB RAM, no CUDA needed):
kwargs = {"device_map": {"": "cpu"}, "torch_dtype": torch.float16}
```

**Patch 7b — input tensor device in `_get_data` (line ~403)**:
```python
# Before:
device = "cuda" if torch.cuda.is_available() else "cpu"

# After:
device = "cpu"  # LLaMA is on CPU — inputs must match
```

---

## Current State

- All 7 patches applied and in place
- `analyze_content.py` unchanged — `config_update` has `batch_size=1` and `device: accelerate`
- `C:\tc\` cache: word-event pipeline (8,356 events) cached — will skip straight to LLaMA embedding step
- **Not yet run with patch 7**

---

## Step 1 — Run the Analysis

```powershell
Get-ChildItem "C:\tc" -Recurse -Filter "inflight.db" | Remove-Item -Force
cd "c:\Users\madhu\Claude cowork\Content Hub V2"
.\.venv-tribe\Scripts\python.exe models/tribev2/analyze_content.py
```

Expect:
- LLaMA fp16 loads to CPU RAM (~6.4 GB)
- TRIBE model stays on GPU (~700 MB)
- 8,356 word embeddings computed on CPU — progress bar visible
- Total runtime: 20–90 min

Expected output shape:
```
============================================================
  Hook — The GitHub repo that gives Claude Code 100 specialized agents
============================================================
  Segments analyzed : N
  Cortical vertices  : 20,484
  Global activation  : X.XXXX  ±Y.YYYY
  Peak TR            : #N  (mean act = X.XXXX)
  Trough TR          : #N  (mean act = X.XXXX)
  Top 5 activated cortical vertices (avg over all TRs):
    #1  vertex XXXXXX  →  X.XXXX
    ...
  Per-TR activation profile:
    TR 000  +X.XXXX  ████████████
    ...
```
Same block repeated for the Outline file.

### If It Still Fails

```powershell
Get-Content "C:\tc\tribe_analysis_err.txt" | Select-Object -Last 30
```

- **CPU RAM OOM**: LLaMA fp16 = ~6.4 GB; OS ~4 GB; should leave ~5 GB free. If OOM, close Chrome/other apps and retry.
- **Device mismatch**: Both model and inputs are on CPU — should not occur. If it does, verify patch 7b is saved.
- **CUDA OOM**: Means a layer leaked to GPU — check `device_map={"": "cpu"}` is present in text.py line ~336.

---

## Step 2 — Interpret the Vertices (NOT Yet Written)

The raw output gives vertex IDs like `vertex 14823 → 0.6721`. These are meaningless without mapping to brain regions. Need to write a short post-processing script using the **fsaverage5 atlas** to convert vertex IDs → region labels (e.g. left superior temporal gyrus = language processing, prefrontal cortex = working memory/attention).

**Script to write** (`models/tribev2/interpret_vertices.py`):
- Load fsaverage5 parcellation labels (available via `nilearn` or `nibabel` + FreeSurfer annot files)
- For each top vertex ID from the analysis output, look up which Desikan-Killiany or Glasser region it belongs to
- Print: `vertex 14823 → left superiortemporal (language network)`

**Key brain regions to watch for in content analysis:**
- Left superior temporal gyrus / STG → language comprehension
- Left inferior frontal gyrus (Broca's area) → syntax, speech production
- Angular gyrus → semantic integration
- Default mode network (medial PFC, precuneus) → narrative, self-referential thought
- Early visual cortex → mental imagery

High activation in language + DMN = content is driving genuine comprehension and mental simulation — good signal for engagement.

---

## Step 3 — Decide How to Use the Signal (Open Decision)

Once you have labeled regions for Hook vs Outline, two paths:

**Option A — One-off analysis**: Use it to understand these two pieces, then move on. No ongoing workflow.

**Option B — Repeatable brain score**: Wire TRIBE into the content pipeline. Every new piece of content gets a "brain score" before publishing — a number or profile showing which networks it activates. Could gate content on minimum language-network activation thresholds.

This decision has not been made. Recommend discussing after seeing the first results.

---

## Full Completion Checklist

- [x] TRIBE v2 installed and all 7 Windows patches applied
- [x] Feature extractors downloaded and cached (LLaMA 3.2-3B, V-JEPA2, Wav2Vec)
- [x] Word-event pipeline cached (8,356 events in `C:\tc\`)
- [ ] **Run `analyze_content.py` and get raw activation output**
- [ ] Write `interpret_vertices.py` — map vertex IDs to brain region labels
- [ ] Compare Hook vs Outline activation profiles
- [ ] Decide: one-off or recurring pipeline integration

---

## All 7 Patches Summary (for re-applying if .venv-tribe is ever rebuilt)

| # | File | What |
|---|------|------|
| 1 | `analyze_content.py` | YAML PosixPath constructor override before `from_pretrained` |
| 2 | `analyze_content.py` | HF login via Python API (`huggingface_hub.login`) not CLI |
| 3 | `analyze_content.py` | `CACHE_FOLDER = r"C:\tc"` — short path avoids Windows MAX_PATH |
| 4 | `tribev2/eventstransforms.py` | Replace `uvx whisperx` subprocess with `faster-whisper` Python API |
| 5 | `exca/cachedict/inflight.py` | Add `except OSError: return False` to `_is_pid_alive` |
| 6 | `analyze_content.py` | `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (harmless on Windows) |
| 7a | `neuralset/extractors/text.py` | `device_map={"": "cpu"}, torch_dtype=float16` — force LLaMA to CPU |
| 7b | `neuralset/extractors/text.py` | Input tensors on `"cpu"` not `"cuda"` |

Modifies: [[TRIBE v2 Local Setup]]
References: [[2026-05-11_TRIBE_v2_Analysis_VRAM_Debug]]
