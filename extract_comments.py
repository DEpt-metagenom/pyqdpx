import pyqdpx
from more_itertools import chunked

qdpx = pyqdpx.QDPX("oltas0517.qdpx")
project = qdpx.get_project()
videos_selection = project.sources['68bbdc14-c361-4432-b4dd-ae1dbfc12890']

start_char = 2
start_chars = []
COMMENT_COLUMN = 5

with open("comments.txt", "w", encoding="utf-8") as comments_file:
    for table_row in chunked(videos_selection.text_content.replace("\r\n\r\n","  \r\n").splitlines(), 8):
        row_prefix_len = len("\t ".join(table_row[:COMMENT_COLUMN]))
        start_chars.append(start_char + row_prefix_len)
        try:
            print(start_chars[-1], start_chars[-1] + len(table_row[COMMENT_COLUMN]), table_row[COMMENT_COLUMN], file=comments_file)
        except IndexError:
            pass
        start_char += len("\t ".join(table_row)) + 2

