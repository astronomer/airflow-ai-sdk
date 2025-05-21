import importlib
import inspect
from pathlib import Path

PACKAGE = Path("airflow_ai_sdk")
DOCS_DIR = Path("docs/interface")
DOCS_DIR.mkdir(parents=True, exist_ok=True)


import subprocess
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
            obj_module = getattr(obj, "__module__", module.__name__)
            if obj_module != module.__name__:
                continue
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

        out_path = DOCS_DIR / path.relative_to(PACKAGE).with_suffix(".md")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with out_path.open("w") as f:
            document_module(module, f)

    # run pre-commit hooks
    subprocess.run(["pre-commit", "run", "--all-files"])  # noqa: S603 S607


if __name__ == "__main__":
    main()
