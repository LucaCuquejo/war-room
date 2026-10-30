# Binance 14 War Room

Tablero privado sobre el drenaje de hot wallets de Binance vía delegación EIP-7702 (29/10/2026): actores, wallets del atacante, congelamientos y declaraciones, en español e inglés.

## Cómo funciona

- `index.html` es una página estática con una landing que pide contraseña.
- `data.enc.json` (datos) y `flujo.enc.json` (infografía) están encriptados con AES-256-GCM; la clave sale de la contraseña con PBKDF2-SHA256 (250.000 iteraciones). El navegador los desencripta solo cuando alguien pone la contraseña correcta.
- Dos tareas programadas de Claude actualizan `data.enc.json` en este repo cada 30 minutos.
- `tools/encrypt_snapshot.py` genera los archivos encriptados:

```bash
python3 tools/encrypt_snapshot.py --password '<contraseña>' --in data.json --out data.enc.json
python3 tools/encrypt_snapshot.py --password '<contraseña>' --in flujo.png --out flujo.enc.json --kind image
```

Nunca subas `data.json` sin encriptar ni la contraseña a este repo.
