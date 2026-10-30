"""Encrypt a file for the Binance 14 War Room page.

Usage:
  python3 encrypt_snapshot.py --password PASS --in data.json --out data.enc [--kind json|image]

Output is a JSON envelope the page decrypts in the browser with WebCrypto:
  {"v":1,"kdf":"PBKDF2-SHA256","iter":250000,"salt":b64,"iv":b64,"ct":b64,"kind":"json"|"image","mime":...}
Key = PBKDF2-SHA256(password, salt, 250000) -> 32 bytes; cipher = AES-256-GCM.
"""
import argparse, base64, json, os, mimetypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 250_000

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--password", required=True)
    p.add_argument("--in", dest="src", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--kind", choices=["json", "image"], default="json")
    a = p.parse_args()
    raw = open(a.src, "rb").read()
    if a.kind == "json":
        json.loads(raw.decode("utf-8"))  # fail early on invalid JSON
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(a.password.encode("utf-8"))
    ct = AESGCM(key).encrypt(iv, raw, None)
    b = lambda x: base64.b64encode(x).decode("ascii")
    env = {"v": 1, "kdf": "PBKDF2-SHA256", "iter": ITER, "salt": b(salt), "iv": b(iv), "ct": b(ct), "kind": a.kind,
           "mime": (mimetypes.guess_type(a.src)[0] or "application/octet-stream") if a.kind == "image" else "application/json"}
    with open(a.out, "w") as f:
        json.dump(env, f)
    print(f"wrote {a.out} ({os.path.getsize(a.out)} bytes)")

if __name__ == "__main__":
    main()
