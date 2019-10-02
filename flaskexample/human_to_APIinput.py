import re
def human_to_APIinput(text):

    end_loc = '+San+Francisco+CA'

    text = re.sub(r"\ ","+",str(text))
    text = text+end_loc
    return text
