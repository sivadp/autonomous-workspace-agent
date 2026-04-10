from pathlib import Path
from typing import Any

class WorkspaceToolbox:
    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self.notes: list[str] = []

    def _resolve_path(self, raw_path: str) -> Path:
        candidate = (self.workspace / raw_path).resolve()
        if self.workspace != candidate and self.workspace not in candidate.parents:
            raise ValueError("Path escapes the workspace.")
        return candidate

    def list_files(self, path: str = ".", recursive: bool = True, limit: int = 200) -> str:
        target = self._resolve_path(path)
        if not target.exists():
            return f"Path not found: {path}"

        items: list[str] = []
        walker = target.rglob("*") if recursive else target.glob("*")
        for item in walker:
            relative = item.relative_to(self.workspace)
            prefix = "[DIR]" if item.is_dir() else "[FILE]"
            items.append(f"{prefix} {relative}")
            if len(items) >= limit:
                items.append("...truncated...")
                break

        if not items:
            return "No files found."
        return "\n".join(items)

    def read_file(self, path: str, max_chars: int = 12000) -> str:
        target = self._resolve_path(path)
        if not target.exists() or not target.is_file():
            return f"File not found: {path}"

        text = target.read_text(encoding="utf-8", errors="replace")
        if len(text) > max_chars:
            text = text[:max_chars] + "\n...truncated..."
        return text

    def write_file(self, path: str, content: str) -> str:
        target = self._resolve_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} characters to {target.relative_to(self.workspace)}"

    def append_file(self, path: str, content: str) -> str:
        target = self._resolve_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as handle:
            handle.write(content)
        return f"Appended {len(content)} characters to {target.relative_to(self.workspace)}"

    def delete_file(self, path: str) -> str:
        target= self._resolve_path(path)
        if target.exists():
            if target.is_file():
                target.unlink()
                return f"Deleted file {target.relative_to(self.workspace)}"
            else:
                return f"Unable to delete because the path is a folder: {target}"
        else:
            return f"File not found: {target}"

    def safe_calc(self, expr: str) -> str:
        allowed = set("0123456789+-*/(). %")
        if not set(expr) <= allowed:
            return "Calculator refused: unsafe characters."
        try:
            result = eval(expr, {"__builtins__": None}, {})
            return str(result)
        except Exception as exc:
            return f"Calculator error: {exc}"

    def save_note(self, text: str) -> str:
        self.notes.append(text)
        return f"Saved note #{len(self.notes)}"

    def get_notes(self) -> str:
        if not self.notes:
            return "No notes yet."
        return "\n".join(f"{idx + 1}. {note}" for idx, note in enumerate(self.notes))

    def describe_tools(self) -> str:
        return (
            "Available tools:\n"
            "- list_files: {'path': '.', 'recursive': true, 'limit': 200}\n"
            "- read_file: {'path': 'relative/path.py', 'max_chars': 12000}\n"
            "- write_file: {'path': 'relative/path.py', 'content': '...'}\n"
            "- append_file: {'path': 'notes.txt', 'content': '...'}\n"
            "- delete_file: {'path': 'notes.txt'}\n"
            "- safe_calc: {'expr': '(12.5*4)/2'}\n"
            "- save_note: {'text': 'important fact'}\n"
            "- get_notes: {}\n"
            "- finish: {'response': 'final answer for the user'}"
        )

    def execute(self, action: str, payload: dict[str, Any]) -> str:
        if action == "list_files":
            return self.list_files(
                path=payload.get("path", "."),
                recursive=payload.get("recursive", True),
                limit=payload.get("limit", 200),
            )
        if action == "read_file":
            return self.read_file(
                path=payload.get("path", ""),
                max_chars=payload.get("max_chars", 12000),
            )
        if action == "write_file":
            return self.write_file(
                path=payload.get("path", ""),
                content=payload.get("content", ""),
            )
        if action == "append_file":
            return self.append_file(
                path=payload.get("path", ""),
                content=payload.get("content", ""),
            )
        if action == "delete_file":
            return self.delete_file(payload.get("path",""))
        if action == "safe_calc":
            return self.safe_calc(payload.get("expr", ""))
        if action == "save_note":
            return self.save_note(payload.get("text", ""))
        if action == "get_notes":
            return self.get_notes()
        if action == "finish":
            return payload.get("response", "")
        return f"Unknown action: {action}"
