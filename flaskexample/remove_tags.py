import re

# parsing html directions fromt he Google Maps API
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    new_text = TAG_RE.sub('', text)
    new_text = re.sub('Destination','\n Destination',new_text)

    return new_text
