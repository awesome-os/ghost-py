# `awesome-os/ghost-py` — Zero-`pip`, Zero-`conda` Native FFI for Python via Ghost CAS

> **Eliminates:** `pip install` C-extension wheel failures, `conda` bloat, virtualenv conflicts, duplicate native binaries.  
> **Canonical Store:** [`awesome-os/b8g-ghost @ cas-v1`](https://github.com/awesome-os/b8g-ghost/releases/tag/cas-v1) (`manifests/index.json`)

## Quick Install & Usage

### Install via `pnpm` (or release tarball)

```powershell
pnpm add github:awesome-os/ghost-py
```

Or download the latest SHA-256 verified archive from [`Releases`](https://github.com/awesome-os/ghost-py/releases/latest).

### Usage & Verification

```powershell
# Hydrate & invoke libbrotli directly from Ghost CAS (pure Python 3 stdlib)
python3 ghost_ffi.py
```

## 1-Line Usage (Pure Python 3 Stdlib — Zero `pip install`)

```python
from ghost_ffi import ghost_open

brotli = ghost_open("libbrotli")
print(hex(brotli.BrotliDecoderVersion()))  # -> 0x1002000 (native C speed, 0 pip installs!)
```

Run live:
```bash
python3 ghost_ffi.py
```
