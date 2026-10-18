import pytest

from nextlaw607.factory_state import FactoryStage, FactoryState


def test_factory_happy_path():
    state = FactoryState()
    for target in (
        FactoryStage.ARCHITECTURE,
        FactoryStage.IMPLEMENT,
        FactoryStage.TEST,
        FactoryStage.REVIEW,
        FactoryStage.VERIFY,
        FactoryStage.COMPLETE,
    ):
        state = state.transition(target)
    assert state.stage is FactoryStage.COMPLETE
    assert state.revision == 6


def test_factory_cannot_skip_verification():
    with pytest.raises(ValueError):
        FactoryState(FactoryStage.REVIEW).transition(FactoryStage.COMPLETE)
