"""Python 표준 라이브러리로 이 폴더의 노트북·번역·로컬 링크를 검사한다.

실행: python ma-drl-satellite-routing/verify_notebooks.py
노트북마다 새 namespace를 사용하며 네트워크·외부 데이터에 접근하지 않는다.
Jupyter UI/kernel 검증을 대신하지 않는다. 저장한 노트북 출력은 변경하지 않는다.
"""

import contextlib
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent


def main():
    notebooks = sorted(ROOT.glob("0*.ipynb"))
    assert len(notebooks) == 3
    for path in notebooks:
        book = json.loads(path.read_text(encoding="utf-8"))
        assert book["nbformat"] == 4 and book["cells"]
        namespace = {"__name__": "__notebook__"}
        cell_ids = [cell["id"] for cell in book["cells"]]
        assert len(cell_ids) == len(set(cell_ids))
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            for index, cell in enumerate(book["cells"]):
                assert cell["cell_type"] in ("code", "markdown")
                assert isinstance(cell["source"], list)
                if cell["cell_type"] == "code":
                    code = "".join(cell["source"])
                    exec(compile(code, f"{path.name}:cell{index}", "exec"), namespace)
        print(f"PASS {path.name}")
        print(stream.getvalue().strip())

    translation = next(ROOT.glob("*.번역.md"))
    content = translation.read_text(encoding="utf-8")
    labels = re.findall(r"\*\*S(\d{3}) — (Original|한국어)\*\*", content)
    expected = [(f"{n:03d}", label) for n in range(1, 109)
                for label in ("Original", "한국어")]
    assert labels == expected, "sentence IDs must be continuous and immediately paired"
    assert "translation.ko.md" not in [p.name for p in ROOT.iterdir()]
    print("PASS translation: 108 paired IDs")

    count = 0
    for path in ROOT.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for raw in re.findall(r"\]\(([^)]+)\)", text):
            target = raw.strip("<>")
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            relative, _, anchor = target.partition("#")
            destination = path.parent / unquote(relative) if relative else path
            assert destination.exists(), f"missing link: {path.name} -> {target}"
            if anchor and destination.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", destination.read_text(encoding="utf-8"), re.M)
                slugs = [re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", h.lower())) for h in headings]
                assert unquote(anchor) in slugs, f"missing anchor: {target}"
            count += 1
    print(f"PASS local Markdown links: {count}")


if __name__ == "__main__":
    main()
