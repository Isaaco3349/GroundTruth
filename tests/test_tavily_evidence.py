from groundtruth.models import EvidencePack
from groundtruth.tavily import evidence as ev


def test_evidence_schema_has_claims():
    assert "claims" in ev.EVIDENCE_SCHEMA["properties"]


def test_pack_from_search_minimal():
    raw = {
        "results": [
            {"url": "https://example.com", "title": "Example", "content": "Snippet text"},
        ]
    }
    pack = ev._pack_from_search("test query", raw)
    assert len(pack.claims) == 1
    assert pack.sources[0].url == "https://example.com"


def test_cache_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(ev, "CACHE_DIR", tmp_path)
    pack = EvidencePack(query="q", claims=[], sources=[], risks=[])
    path = ev._cache_path("q", "search")
    ev._save_cache(path, pack)
    loaded = ev._load_cache(path)
    assert loaded is not None
    assert loaded.query == "q"
