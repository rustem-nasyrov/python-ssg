def markdown_to_blocks(markdown):
    rows = markdown.strip().split("\n\n")

    filter(lambda s: len(s) > 0, rows)

    for i in range(0, len(rows)):
        rows[i] = rows[i].strip()

    return rows
