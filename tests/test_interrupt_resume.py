from nextlaw607.execution_state import CheckpointStore, RunScope
from nextlaw607.interrupt_resume import InterruptResumeCoordinator


def test_interrupt_checkpoint_and_resume(tmp_path):
    scope = RunScope("u1", "matter-a", "research", "run-1")
    coordinator = InterruptResumeCoordinator(CheckpointStore(tmp_path))
    state = coordinator.checkpoint(
        scope,
        phase="verify",
        payload={"cursor": 7},
        expected_revision=0,
    )
    assert state.revision == 1
    assert coordinator.resume(scope) == state


def test_resume_is_scope_exact(tmp_path):
    coordinator = InterruptResumeCoordinator(CheckpointStore(tmp_path))
    a = RunScope("u1", "matter-a", "research", "run-1")
    b = RunScope("u1", "matter-b", "research", "run-1")
    coordinator.checkpoint(a, phase="collect", payload={}, expected_revision=0)
    assert coordinator.resume(b) is None
