from nextlaw607.features.citation_graph import expand

def test_graph_expands_only_requested_depth():
    edges={"a":["b"],"b":["c"]}
    assert expand(["a"], edges, depth=1) == ("a","b")
    assert expand(["a"], edges, depth=2) == ("a","b","c")
