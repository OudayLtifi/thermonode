from gateway.storage import RETENTION_S, Storage


def test_purge_removes_expired_measure_and_close(tmp_path):
    storage = Storage(tmp_path / "gw.sqlite")
    storage.insert("TN01", 1, 100, 25.0, "NORMAL", now=100)
    storage.insert("TN01", 2, 200, 25.0, "NORMAL", now=200)

    removed = storage.purge(now=100 + RETENTION_S + 1)

    assert removed == 1
    assert storage.count() == 1
    storage.close()
