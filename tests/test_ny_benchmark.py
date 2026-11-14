from nextlaw607.features.ny_benchmark import evaluate

def test_benchmark_counts_accuracy_and_fail_closed():
    r=evaluate(["suppression","unknown"],["suppression","appeal"])
    assert (r.total,r.correct,r.failed_closed)==(2,1,1)
    assert r.accuracy==0.5
