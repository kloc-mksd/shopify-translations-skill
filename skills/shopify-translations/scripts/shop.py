"""Admin API helpers. Credentials come from .env in the current directory:
SHOPIFY_STORE (xxx.myshopify.com) and SHOPIFY_ACCESS_TOKEN
(scopes: read_translations, write_translations, read_products, read_themes,
read_content, read_online_store_navigation, read_metaobjects)."""
import json, os, time, requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), ".env"))
STORE = os.getenv("SHOPIFY_STORE")
URL = f"https://{STORE}/admin/api/2025-10/graphql.json"
H = {"X-Shopify-Access-Token": os.getenv("SHOPIFY_ACCESS_TOKEN") or "", "Content-Type": "application/json"}
WORK = os.path.join(os.getcwd(), "translations-work")


def gql(q, v=None):
    for attempt in range(8):
        try:
            r = requests.post(URL, headers=H, json={"query": q, "variables": v or {}}, timeout=120)
            if r.status_code in (429, 502, 503, 504):
                raise RuntimeError(r.status_code)
            d = r.json()
        except (requests.RequestException, ValueError, RuntimeError):
            time.sleep(2 + attempt * 2)
            continue
        if "THROTTLED" in json.dumps(d.get("errors", "")):
            time.sleep(3 + attempt * 2)
            continue
        if d.get("errors"):
            raise RuntimeError(d["errors"])
        return d["data"]
    raise RuntimeError("Admin API unreachable or throttled")


def bulk(query):
    """Run a bulk query, return parsed JSONL rows."""
    op = gql('mutation($q:String!){bulkOperationRunQuery(query:$q){bulkOperation{id} userErrors{message}}}',
             {"q": query})["bulkOperationRunQuery"]
    if op["userErrors"]:
        raise RuntimeError(op["userErrors"])
    oid = op["bulkOperation"]["id"]
    while True:
        time.sleep(4)
        n = gql('query($id:ID!){node(id:$id){...on BulkOperation{status errorCode url}}}', {"id": oid})["node"]
        if n["status"] == "COMPLETED":
            return [json.loads(l) for l in requests.get(n["url"], timeout=600).text.splitlines()] if n["url"] else []
        if n["status"] in ("FAILED", "CANCELED", "EXPIRED"):
            raise RuntimeError(f"bulk {n['status']} {n['errorCode']}")


def shop_info():
    d = gql('{ shop{myshopifyDomain} shopLocales{locale primary published} themes(first:1, roles:[MAIN]){nodes{id name}} }')
    locales = [l["locale"] for l in d["shopLocales"] if l["published"] and not l["primary"]]
    return d["shop"]["myshopifyDomain"], locales, d["themes"]["nodes"][0]


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def write_jsonl(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
