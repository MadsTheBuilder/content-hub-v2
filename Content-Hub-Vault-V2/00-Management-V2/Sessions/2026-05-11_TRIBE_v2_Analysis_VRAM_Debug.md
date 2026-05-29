---
date: 2026-05-11
type: session-log
status: in-progress — handoff
---

# TRIBE v2 fMRI Analysis — VRAM Debug Session

## Goal
Run `analyze_content.py` to get fMRI brain-activation predictions for two vault content files:
- `05-Hooks/2026-05-06_the-github-repo-that-gives-claude.md`
- `06-Outlines/2026-05-06_why-ruflo-is-a-must-use.md`

## What Works
- [[TRIBE v2 Local Setup]] — model loads cleanly
- faster-whisper transcription — 8,368 words extracted from Hook TTS audio, cached in `C:\tc\`
- spaCy en-core-web-lg + AddContextToWords pipeline — complete, cached
- bitsandbytes 4-bit quantization — LLaMA 3.2-3B loads as ~1.75 GB (down from 6 GB fp16)
- `exca/cachedict/inflight.py` Windows patch — `OSError` on `os.kill(pid, 0)` handled

## Current Blocker — CUDA OOM in Attention Forward Pass

**Error**: `torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 3.40 GiB.`  
**Where**: `transformers/integrations/sdpa_attention.py:96` → `scaled_dot_product_attention`  
**Root cause**: LLaMA 3.2-3B's attention with batch_size=4 and context_len=1024 requires a 3.40 GiB allocation for the attention tensor. Even with 4-bit quantization (LLaMA ~1.75 GB on GPU + TRIBE ~700 MB), the forward-pass activation spike exceeds the remaining ~5.5 GB of free VRAM.

## The Fix (NOT YET APPLIED)

In `models/tribev2/analyze_content.py`, change `config_update` to:

```python
config_update={
    "data.text_feature.device": "accelerate",
    "data.text_feature.batch_size": 1,   # ← ADD THIS
},
```

`batch_size: 1` reduces the attention allocation from ~3.4 GB → ~850 MB (4x smaller), which fits.

Current line in [analyze_content.py](../../../models/tribev2/analyze_content.py#L105):
```python
config_update={"data.text_feature.device": "accelerate"},
```

## Files Modified This Session (All Patches Applied)

| File | Change |
|---|---|
| `models/tribev2/analyze_content.py` | Main analysis script; `CACHE_FOLDER=r"C:\tc"`, YAML PosixPath patch, HF login, 4-bit config, `PYTORCH_CUDA_ALLOC_CONF` env var |
| `.venv-tribe\Lib\site-packages\tribev2\eventstransforms.py` | Replaced `uvx whisperx` subprocess with `faster-whisper` Python API (lines 95–139) |
| `.venv-tribe\Lib\site-packages\neuralset\extractors\text.py` | Added bitsandbytes 4-bit quantization to `device=="accelerate"` branch (lines 335–341) |
| `.venv-tribe\Lib\site-packages\exca\cachedict\inflight.py` | Added `except OSError: return False` to `_is_pid_alive` (lines 64–72) |

## Installed Packages (New This Session)

- `torch==2.6.0+cu124` — replaces CPU-only `torch==2.6.0` (was missing CUDA)
- `accelerate==1.13.0`
- `bitsandbytes==0.49.2`
- spaCy `en-core-web-lg==3.8.0` — downloaded automatically by tribev2

## exca Cache State

All successful steps are cached at `C:\tc\`. On the next run, exca will skip:
- TTS audio generation (audio.mp3 exists)
- faster-whisper transcription (audio.tsv exists)
- AddContextToWords pipeline (8,368 word events cached)

The text embedding step (LLaMA forward pass) will re-run because `batch_size` is changing (new exca UID).

**IMPORTANT**: Before each run, delete stale inflight.db files:
```powershell
Get-ChildItem "C:\tc" -Recurse -Filter "inflight.db" | Remove-Item -Force
```

## Run Command

From project root:
```powershell
Get-ChildItem "C:\tc" -Recurse -Filter "inflight.db" | Remove-Item -Force
.\.venv-tribe\Scripts\python.exe models/tribev2/analyze_content.py
```

## Expected Output (After Fix)

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

Same format for the Outline file.

## What Comes After

Once we have the activation profiles:
1. Interpret which cortical regions correspond to the top vertices (use fsaverage5 atlas)
2. Compare Hook vs Outline — which drives more language-network activation?
3. Potentially iterate on content based on fMRI signal (higher early-language-cortex activation = better engagement)

Modifies: [[TRIBE v2 Local Setup]]
References: [[2026-05-11_Phase0_Cleanup]]
