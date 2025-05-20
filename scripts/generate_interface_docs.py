import importlib
import inspect
from pathlib import Path

PACKAGE = Path("airflow_ai_sdk")
DOCS_DIR = Path("docs/interface")
DOCS_DIR.mkdir(parents=True, exist_ok=True)


from types import ModuleType
from typing import TextIO


def document_module(module: ModuleType, file: TextIO) -> None:
    file.write(f"# {module.__name__}\n\n")
    if module.__doc__:
        file.write(inspect.getdoc(module))
        file.write("\n\n")
    for name, obj in inspect.getmembers(module):
        if name.startswith("_"):
            continue
        if inspect.isfunction(obj) or inspect.isclass(obj):
            file.write(f"## {name}\n\n")
            doc = inspect.getdoc(obj) or "No documentation."
            file.write(doc)
            file.write("\n\n")


def main() -> None:
    for path in PACKAGE.rglob("*.py"):
        if path.name == "__init__.py":
            continue
        module_name = path.with_suffix("").as_posix().replace("/", ".")
        module = importlib.import_module(module_name)
        out_file = DOCS_DIR / f"{module_name.replace('.', '_')}.md"
        with out_file.open("w") as f:
            document_module(module, f)


if __name__ == "__main__":
    main()
