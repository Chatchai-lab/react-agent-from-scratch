import pytest

from src.tools import file_system


@pytest.fixture(autouse=True)
def sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(file_system, "WORKSPACE_ROOT", tmp_path.resolve())
    return tmp_path


def test_write_then_read_roundtrip():
    write_result = file_system.write_file.run({"path": "notes.txt", "content": "hallo"})
    assert "erfolgreich" in write_result
    assert file_system.read_file.run({"path": "notes.txt"}) == "hallo"


def test_read_nonexistent_file():
    result = file_system.read_file.run({"path": "missing.txt"})
    assert "Fehler" in result


def test_read_path_traversal_blocked():
    result = file_system.read_file.run({"path": "../../etc/passwd"})
    assert "außerhalb der Sandbox" in result


def test_read_absolute_path_blocked():
    result = file_system.read_file.run({"path": "/etc/passwd"})
    assert "außerhalb der Sandbox" in result


def test_write_path_traversal_blocked(sandbox):
    result = file_system.write_file.run({"path": "../evil.txt", "content": "x"})
    assert "außerhalb der Sandbox" in result
    assert not (sandbox.parent / "evil.txt").exists()


def test_read_rejects_oversized_file(sandbox):
    big_file = sandbox / "big.txt"
    big_file.write_text("x" * (file_system.MAX_READ_BYTES + 1))
    result = file_system.read_file.run({"path": "big.txt"})
    assert "zu groß" in result


def test_write_rejects_oversized_content():
    too_big = "x" * (file_system.MAX_WRITE_BYTES + 1)
    result = file_system.write_file.run({"path": "big.txt", "content": too_big})
    assert "zu groß" in result
