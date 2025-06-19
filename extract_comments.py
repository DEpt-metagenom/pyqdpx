import pyqdpx
import json
from more_itertools import chunked

qdpx = pyqdpx.QDPX("oltas0517.qdpx")
project = qdpx.get_project()
videos_selection = project.sources['68bbdc14-c361-4432-b4dd-ae1dbfc12890']

start_char = 2
start_chars = []

VIDEO_ID_COLUMN = 0
USER_COLUMN = 4
COMMENT_COLUMN = 5

comments_dict = {}

with open("comments.txt", "w", encoding="utf-8") as comments_file:
    for table_row in chunked(videos_selection.text_content.replace("\r\n\r\n5","  \r\n5").splitlines(), 8):
        video_id = table_row[VIDEO_ID_COLUMN].strip()
        if video_id not in comments_dict:
            comments_dict[video_id] = []
        if len(video_id) != 11 and video_id != "video_id":
            raise ValueError(f"Invalid video ID: {video_id} in row {table_row}")
        row_prefix_len = len("\t ".join(table_row[:COMMENT_COLUMN]))
        start_chars.append(start_char + row_prefix_len)
        user_name = table_row[USER_COLUMN].strip()
        comment_data = {'user': user_name if user_name else "---",
                        'comment': table_row[COMMENT_COLUMN].strip().replace("\u200b", ""),
                        'start': start_char + row_prefix_len,
                        'end': start_char + row_prefix_len + len(table_row[COMMENT_COLUMN])}
        comments_dict[video_id].append(comment_data)        
        try:
            print(start_chars[-1], start_chars[-1] + len(table_row[COMMENT_COLUMN]), table_row[COMMENT_COLUMN], file=comments_file)
        except IndexError:
            print(f"Error processing row: {table_row}")
        start_char += len("\t ".join(table_row)) + 2

with open("comments.json", "w", encoding="utf-8") as json_file:
    json.dump(comments_dict, json_file, ensure_ascii=False, indent=4)
