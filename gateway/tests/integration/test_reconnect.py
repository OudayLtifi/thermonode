"""ENF-05 : mémorisation et retransmission après coupure du broker."""
import pytest
import time

pytestmark = pytest.mark.integration


@pytest.mark.timeout(180)
def test_ENF05_buffered_measures_are_resent_after_broker_outage(
    node, broker, gateway
):
    node.inject_measures([25.0] * 5)
    gateway.wait_for_frames(min_count=1, timeout_s=30)
    n0 = len(gateway.frames)

    broker.stop()
    node.inject_connection(False)
    node.inject_measures([25.1] * 30)
    time.sleep(15)

    broker.start()
    node.inject_connection(True)
    frames = gateway.wait_for_frames(min_count=n0 + 3, timeout_s=60)
    seqs = [f["seq"] for f in frames]
    assert seqs == sorted(seqs) and len(set(seqs)) == len(seqs), (
        f"trous ou doublons : {seqs}"
    )
