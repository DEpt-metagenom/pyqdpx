import pyqdpx
from more_itertools import chunked

qdpx = pyqdpx.QDPX("oltas.qdpx")
project = qdpx.get_project()
videos_selection = project.sources['56a79789-d535-4fb8-bedd-a915504c54ba']

start_char = 2
start_chars = []
COMMENT_COLUMN = 5

with open("comments.txt", "w", encoding="utf-8") as comments_file:
    for table_row in chunked(videos_selection.text_content.splitlines(), 8):
        row_prefix_len = len("\t ".join(table_row[:COMMENT_COLUMN]))
        start_chars.append(start_char + row_prefix_len)
        print(start_chars[-1], start_chars[-1] + len(table_row[COMMENT_COLUMN]), table_row[COMMENT_COLUMN], file=comments_file)
        start_char += len("\t ".join(table_row)) + 2

