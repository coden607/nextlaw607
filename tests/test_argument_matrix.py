import pytest
from nextlaw607.features.argument_matrix import build

def test_matrix_requires_adversarial_and_review_fields():
    rows=build([{"issue":"suppression","argument":"exclude","counterargument":"attenuation","burden":"People","standard_of_review":"mixed","authority_ids":["a1"]}])
    assert rows[0].counterargument=="attenuation"
    with pytest.raises(ValueError):
        build([{"issue":"x","argument":"a","counterargument":"","burden":"b","standard_of_review":"s","authority_ids":["a1"]}])
