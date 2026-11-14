from nextlaw607.features.preservation_matrix import assess

def test_matrix_distinguishes_preservation_and_standard():
    x=assess(objection=True,ruling=True,constitutional=True)
    assert x["preserved"] is True
    assert x["harmless_error_standard"]=="constitutional"
