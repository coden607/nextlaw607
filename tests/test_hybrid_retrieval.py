from nextlaw607.features.hybrid_retrieval import fuse

def test_fusion_rewards_cross_ranker_support():
    out = dict(fuse(["a","b","c"], ["b","d","a"]))
    assert out["a"] > out["c"]
    assert out["b"] > out["d"]

def test_fusion_tie_breaks_deterministically():
    assert [doc for doc, _ in fuse(["b"], ["a"])] == ["a", "b"]
