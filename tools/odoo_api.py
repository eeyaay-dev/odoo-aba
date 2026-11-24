"""Tiny read-only client for the Odoo 19 JSON-2 API.

Reads ODOO_URL / ODOO_API_KEY (and optional ODOO_DB) from the repo's .env.
Write methods are refused unless allow_write=True is passed explicitly.

Usage from Python:
    from odoo_api import call
    call("res.partner", "search_read", domain=[], fields=["name"], limit=5)

Usage from the shell (prints JSON):
    python tools/odoo_api.py res.users context_get
    python tools/odoo_api.py res.partner search_read '{"domain": [], "fields": ["name"], "limit": 5}'
"""
import json
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent

READ_METHODS = {
    "search_read", "read", "search", "search_count", "fields_get",
    "read_group", "formatted_read_group", "context_get", "name_search",
    "get_param", "default_get", "get_views",
}


def _load_env(path):
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


_ENV = _load_env(ROOT / ".env")
URL = _ENV["ODOO_URL"].rstrip("/")
_KEY = _ENV["ODOO_API_KEY"]
_DB = _ENV.get("ODOO_DB")


def call(model, method, allow_write=False, **kwargs):
    if method not in READ_METHODS and not allow_write:
        raise PermissionError(f"{model}.{method} is not a read method (pass allow_write=True)")
    req = urllib.request.Request(
        f"{URL}/json/2/{model}/{method}",
        data=json.dumps(kwargs).encode("utf-8"),
        method="POST",
    )
    req.add_header("Authorization", f"bearer {_KEY}")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("User-Agent", "odoo-aba-tools")
    if _DB:
        req.add_header("X-Odoo-Database", _DB)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            return json.loads(body) if body else None
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {err.code} on {model}.{method}: {detail[:2000]}") from None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    result = call(sys.argv[1], sys.argv[2], **params)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
