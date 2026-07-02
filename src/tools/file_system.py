from pathlib import Path

from src.tools.base import Tool

WORKSPACE_ROOT = (Path(__file__).resolve().parent.parent.parent / "workspace").resolve()
WORKSPACE_ROOT.mkdir(exist_ok=True)

MAX_READ_BYTES = 100_000
MAX_WRITE_BYTES = 100_000


def _resolve_safe_path(relative_path: str) -> Path:
    try:
        candidate = (WORKSPACE_ROOT / relative_path).resolve()
    except OSError as e:
        raise ValueError(f"Ungültiger Pfad: {e}")
    if not candidate.is_relative_to(WORKSPACE_ROOT):
        raise ValueError(f"Pfad außerhalb der Sandbox: {relative_path}")
    return candidate


class ReadFileTool(Tool):
    name = "read_file"
    description = "Reads a text file from the sandboxed workspace directory and returns its content."
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path relative to the workspace directory, e.g. 'notes.txt'"},
        },
        "required": ["path"],
    }

    def run(self, args: dict) -> str:
        try:
            path = _resolve_safe_path(args["path"])
        except ValueError as e:
            return f"Fehler: {e}"

        if not path.exists():
            return f"Fehler: Datei '{args['path']}' existiert nicht."
        if not path.is_file():
            return f"Fehler: '{args['path']}' ist keine Datei."

        size = path.stat().st_size
        if size > MAX_READ_BYTES:
            return f"Fehler: Datei zu groß ({size} Bytes, Limit {MAX_READ_BYTES} Bytes)."

        try:
            return path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError, OSError) as e:
            return f"Fehler beim Lesen von '{args['path']}': {e}"


class WriteFileTool(Tool):
    name = "write_file"
    description = "Writes text content to a file in the sandboxed workspace directory (creates or overwrites)."
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path relative to the workspace directory, e.g. 'notes.txt'"},
            "content": {"type": "string", "description": "The text content to write"},
        },
        "required": ["path", "content"],
    }

    def run(self, args: dict) -> str:
        try:
            path = _resolve_safe_path(args["path"])
        except ValueError as e:
            return f"Fehler: {e}"

        content = args["content"]
        if len(content.encode("utf-8")) > MAX_WRITE_BYTES:
            return f"Fehler: Inhalt zu groß (Limit {MAX_WRITE_BYTES} Bytes)."

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        except (PermissionError, OSError) as e:
            return f"Fehler beim Schreiben von '{args['path']}': {e}"

        return f"Datei '{args['path']}' erfolgreich geschrieben ({len(content)} Zeichen)."


read_file = ReadFileTool()
write_file = WriteFileTool()
