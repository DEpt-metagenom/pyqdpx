import json
import yaml
import pyqdpx
# import ollama

qdpx = pyqdpx.QDPX("oltas0517.qdpx")
project = qdpx.get_project()

with open('comments.json', encoding='utf-8') as file:
    data = json.load(file)

video_ids = list(data.keys())[1:25]

with open('videos.yaml.old2') as file:
    videos = yaml.safe_load(file)
    video_dict = {video['id']: video for video in videos}

for video_id in video_ids:
    print(video_id)
    print("Title:", video_dict[video_id]['title'])
    print("Description:", video_dict[video_id]['description'])
    print("Comments:")
    for comment in data[video_id]:
        print(f"- {comment['user']}: {comment['comment']}")

labels = [
    'Conspiracist ideation: This attitude root reflects a tendency to believe in conspiracy theories—defined as the unnecessary assumption of conspiracy when other explanations are more probable.',
]

prompt = f"""The following are the title, description and some comments of a Hungarian YouTube video.
You are an annotator whose task is to decide whether each comment should receive a specific label.
This is for a sociological study that aims to understand negative attitudes towards vaccines and vaccination.
All labels are understood as binary labels, meaning that a comment can either receive the label or not.
They should be applied to a comment as a whole. The question is whether the label describes the
negative attitude of the posting user towards vaccines and vaccination correctly.
Only apply the label if the comment expresses the specific attitude described by the label explicitly.
For example, if the label says "vaccine causes autism", only apply the label if the comment explicitly
appears to subscribe to the claim or assumes that it is true that vaccines cause autism.
You can use the title, description and the other comments as context:
[title]{video_dict[video_id]['title']}[/title]
[description]{video_dict[video_id]['description']}[/description]
[comments]
{[f"- [user_name]{comment['user']}[/user]: {comment['comment']}" for comment in data[video_id]]}
[/comments]
Does the following comment express the attitude described by the label? Consider what the user is saying, then answer with yes or no.
Keep in mind that users often use sarcasm, irony, or other rhetorical devices that may not directly express the attitude.
The linguistic quality of the comments tends to be low, punctuation, grammar, and spelling errors are common.
Often it is completely unclear what the user is trying to say, or the comment is so short that it is impossible to interpret it.
Keep this in mind when trying to interpret the comment.
This is the label to be considered:
[label]{labels[0]}[/label]
This is the specific comment to be either labeled or not:
[comment]{data[video_id][0]['comment']}[/comment]
The last word in your answer should be either "yes" or "no" accordingly.
"""

print(prompt)