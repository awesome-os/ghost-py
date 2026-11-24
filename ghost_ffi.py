"""
ghost_ffi.py — Zero-pip, zero-conda O(1) Ghost CAS native FFI loader for Python 3.
Hydrates native shared libraries from awesome-os/b8g-ghost @ cas-v1 into the shared
Machine CAS with FIPS 180-4 SHA-256 verification and loads them via ctypes.CDLL.
"""
import ctypes
import hashlib
import json
import os
import platform
import sys
import urllib.request
from pathlib import Path

INDEX_URL = "https://raw.githubusercontent.com/awesome-os/b8g-ghost/main/manifests/index.json"
CAS_BASE = "https://github.com/awesome-os/b8g-ghost/releases/download/cas-v1/"


def machine_cas_dir() -> Path:
    if os.environ.get("B8G_CAS_DIR"):
        return Path(os.environ["B8G_CAS_DIR"])
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / "AwesomeOS" / "cas"
    return Path.home() / ".local" / "share" / "awesome-os" / "cas"


def platform_filename(base_name: str) -> str:
    if "." in base_name:
        return base_name
    arch = "arm64" if platform.machine().lower() in ("arm64", "aarch64") else "x64"
    if sys.platform == "win32":
        return f"{base_name}-win64.dll"
    if sys.platform == "darwin":
        return f"{base_name}-macos-{arch}.dylib"
    return f"{base_name}-linux-{arch}.so"


def resolve(base_name: str) -> tuple[Path, bool]:
    filename = platform_filename(base_name)
    with urllib.request.urlopen(INDEX_URL) as resp:
        idx = json.loads(resp.read().decode("utf-8"))
    entry = idx["entries"].get(filename)
    if not entry:
        raise KeyError(f"Asset '{filename}' not found in canonical Ghost CAS index")
    expected_sha = entry["sha256"].lower()
    target_dir = machine_cas_dir() / expected_sha
    target = target_dir / filename

    if target.exists():
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual == expected_sha:
            return target, True

    with urllib.request.urlopen(CAS_BASE + expected_sha) as resp:
        data = resp.read()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected_sha:
        raise ValueError(f"Ghost SHA-256 mismatch for {filename}: expected {expected_sha}, got {actual}")

    target_dir.mkdir(parents=True, exist_ok=True)
    tmp = target_dir / f"{filename}.tmp.{os.getpid()}"
    tmp.write_bytes(data)
    os.replace(tmp, target)
    return target, False


def ghost_open(base_name: str) -> ctypes.CDLL:
    path, hit = resolve(base_name)
    print(f"[ghost-py] [{'CAS-HIT ' if hit else 'HYDRATED'}] {path.name} -> {path}")
    return ctypes.CDLL(str(path))


if __name__ == "__main__":
    brotli = ghost_open("libbrotli")
    brotli.BrotliDecoderVersion.restype = ctypes.c_uint32
    ver = brotli.BrotliDecoderVersion()
    assert ver > 0x01000000, f"Unexpected Brotli version: {hex(ver)}"
    print(f"[ghost-py] LIVE Native BrotliDecoderVersion() = {hex(ver)} (0 pip installs!)")
