# `awesome-os/ghost-py` — Zero-`pip`, Zero-`conda` Native FFI for Python via Ghost CAS

> **Eliminates:** `pip install` C-extension wheel failures, `conda` bloat, virtualenv conflicts, duplicate native binaries.  
> **Canonical Store:** [`awesome-os/b8g-ghost @ cas-v1`](https://github.com/awesome-os/b8g-ghost/releases/tag/cas-v1) (`manifests/index.json`)

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
