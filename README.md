# Local Peer Starter Kit v1.0

One-command local AI stack. Docker compose everything, zero cloud dependencies.

## The Stack

| Component | Tool | Role |
| --- | --- | --- |
| Inference | Ollama | LLM backend |
| Interface | Open WebUI | Chat frontend (with RAG) |
| Memory | Qdrant | Vector database (scales beyond the default Chroma) |

All data stays on your machine. No telemetry. No API keys required.

## Requirements

- **GPU:** NVIDIA with CUDA (RTX 3090/4090 or equivalent)
- **VRAM:** 8GB minimum for 7B models, 24GB+ for anything good
- **RAM:** 16GB+, 32GB recommended (models + WebUI + Qdrant)
- **Disk:** 50GB free (OS + Docker + models). A single 8B model is ~5GB; larger ones go up.
- **OS:** Ubuntu 22.04+ (drivers, Docker, nvidia-container-toolkit)

## Setup

1. Clone and cd in:

   ```bash
   git clone https://github.com/CocaKova/local-peer-starter-kit.git
   cd local-peer-starter-kit
   ```

2. Run the setup script:

   ```bash
   ./setup.sh
   ```

   This checks for NVIDIA drivers and Docker, generates a random `.env` with a secure secret, then pulls and starts the containers.

3. Open [http://localhost:3000](http://localhost:3000).

4. Go to **Settings → Models** and pull your first model.

   The first model pull takes a while (5-20 minutes depending on your connection and model size). Ollama caches it on disk, so subsequent starts are instant.

### What's running where

| Service | URL |
| --- | --- |
| Open WebUI (chat) | `http://localhost:3000` |
| Ollama API | `http://localhost:11434` |
| Qdrant Dashboard | `http://localhost:6333/dashboard` |

## Configuration

Everything is in `.env`. You rarely need to touch it after setup, but here are the options:

- `OLLAMA_PORT` — Ollama API port (default: 11434)
- `WEBUI_PORT` — Open WebUI port (default: 3000)
- `WEBUI_SECRET_KEY` — Generated automatically on first run
- `QDRANT_PORT` — Qdrant API port (default: 6333)
- `QDRANT_STORAGE_PATH` — Where embeddings persist

## Non-NVIDIA

- **AMD GPU:** Run Ollama from source instead of the container.
- **Apple Silicon:** Open WebUI supports MPS. Check their docs for details.

## License

MIT — do whatever with it.