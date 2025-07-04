"""
🧠 Intelligent MCP Image Search Server
Run:
    python imageSearchMCP.py --name MyImageMCP --debug
"""

import os
import logging
import argparse
import requests
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image
from fastmcp import FastMCP

# ───── ENV ─────────────────────────────────────────────────────────
load_dotenv()
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# ───── ARGS ────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Unsplash Image MCP Server")
parser.add_argument("--name", type=str, default="ImageSearchMCP", help="Server name")
parser.add_argument("--debug", action="store_true", help="Enable debug logging")
args = parser.parse_args()

# ───── LOGGING ─────────────────────────────────────────────────────
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(
    level=log_level,
    format="[%(asctime)s] %(levelname)-8s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S"
)

# ───── MCP INSTANCE ────────────────────────────────────────────────
server_name = args.name + (" (Debug)" if args.debug else "")
mcp = FastMCP(server_name)

# ───── IMAGE SCORING ───────────────────────────────────────────────
def score_image(image: Image.Image) -> int:
    width, height = image.size
    resolution_score = min((width * height) / (1024 * 768), 1.0) * 40
    aspect_ratio = width / height
    aspect_score = 20 if 1.3 <= aspect_ratio <= 1.8 else 10
    sharpness_score = 20  # Placeholder
    compression_score = 20  # Placeholder
    return int(min(resolution_score + aspect_score + sharpness_score + compression_score, 100))

# ───── API FETCH ───────────────────────────────────────────────────
def fetch_image_urls(query: str, limit: int) -> list[str]:
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {"query": query, "per_page": limit}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return [img["urls"]["regular"] for img in data.get("results", [])]
    except Exception as e:
        logging.warning(f"❌ Unsplash API error: {e}")
        return []

# ───── CORE LOGIC ──────────────────────────────────────────────────
def _image_search_logic(query: str, max_results: int, min_score: int, min_resolution: list[int]) -> list[dict]:
    logging.info(f"🔍 Searching Unsplash for: '{query}'")
    urls = fetch_image_urls(query, max_results * 2)
    results = []

    for url in urls:
        try:
            resp = requests.get(url, timeout=5)
            image = Image.open(BytesIO(resp.content))
            width, height = image.size
            if width < min_resolution[0] or height < min_resolution[1]:
                continue
            score = score_image(image)
            if score >= min_score:
                results.append({
                    "url": url,
                    "score": score,
                    "resolution": f"{width}x{height}"
                })
        except Exception:
            continue

    logging.info(f"✅ {len(results)} image(s) passed quality check")
    return sorted(results, key=lambda x: -x["score"])[:max_results]

# ───── MCP TOOL ────────────────────────────────────────────────────
@mcp.tool
def image_search(
    query: str,
    max_results: int = 10,
    min_quality_score: int = 80,
    min_resolution: list[int] = [1024, 768]
) -> list[dict]:
    return _image_search_logic(query, max_results, min_quality_score, min_resolution)

# ───── OPTIONAL STATUS TOOL ────────────────────────────────────────
@mcp.tool
def status() -> dict:
    return {
        "server_name": server_name,
        "debug": args.debug,
        "api_key_loaded": bool(UNSPLASH_ACCESS_KEY),
    }

# ───── ENTRYPOINT ──────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    # mcp.run()  # no transport param = stdio mode
