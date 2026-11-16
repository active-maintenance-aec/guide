# Post-render: publish the Markdown sources beside the HTML, and write llms.txt
# (an index of those sources) and llms-full.txt (the whole guide in one file),
# both in the sidebar's reading order, so an agent can read the guide in one fetch.

import os
import re
import shutil
from pathlib import Path

site_url = "https://active-maintenance-aec.github.io/guide"
out_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))

sidebar = Path("_quarto.yml").read_text().split("  sidebar:", 1)[1]
pages = re.findall(r"(?:- |href: )([\w/]+\.(?:md|qmd))\s*$", sidebar, flags=re.M)
pages = ["README.md" if page == "index.qmd" else page for page in pages]

def title(text):
    return re.search(r"^# (.+)$", text, flags=re.M).group(1).replace("`", "")

index = [
    "# Active maintenance: a guide",
    "",
    "> How we actively maintained the replication archives of published papers with AI coding agents: "
    "the stages, the rules for judging errors, the output table schemas, known traps, and instructions written for agents.",
    "",
    f"The whole guide in one file: {site_url}/llms-full.txt",
    "",
    "## Pages, in reading order",
    "",
]
full = []

for page in pages:
    text = Path(page).read_text()
    target = out_dir / page
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(page, target)
    index.append(f"- [{title(text)}]({site_url}/{page})")
    full.append(f"<!-- file: {page} -->\n\n{text.strip()}\n")

(out_dir / "llms.txt").write_text("\n".join(index) + "\n")
(out_dir / "llms-full.txt").write_text("\n\n".join(full))
