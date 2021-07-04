# %%

from datetime import datetime
import arxiv
import latexcodec
from tomark import Tomark
import urllib

# %%


def d(s):
    return s.encode("ascii").decode("latex")


# %%

search = arxiv.Search(
    query='ti:"all you need"',
    max_results=float("inf"),
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Ascending,
)

table = []

for result in search.get():
    etal = " et al." if len(result.authors) > 1 else ""
    if any([s.startswith("cs") for s in result.categories]):
        table.append(
            {
                "Title": f"[{d(result.title)}]({result.entry_id})",
                "Authors": f"{result.authors[0].name}{etal}",
                "Date": str(result.published).split(" ")[0],
            }
        )

# %%
def remove_date(s):
    val = ""
    for line in s.splitlines():
        if not line.startswith('![Last Added]'):
            val += line + "\n"
    return val

# %%

with open("template.md", "r", encoding="utf8") as file:
    data = file.read().replace("[PAPER LIST]", Tomark.table(table))
with open("readme.md", "r", encoding="utf8") as file:
    if remove_date(file.read()) != remove_date(data):
        with open("readme.md", "w", encoding="utf8") as f:
            f.writelines(
                data.replace(
                    "DATEHERE", 
                    table[-1]["Date"]
                    # str(datetime.today()).split(" ")[0].replace("-", "--")
                )
            )
