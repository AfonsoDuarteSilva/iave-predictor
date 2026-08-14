from difflib import SequenceMatcher


def normalize_topics(list_topics, limit):
    result_list = []
    for topic in list_topics:
        found_similar = False 

        for norm_topic in result_list:
            if is_similar(topic["name"], norm_topic["name"], limit):
                found_similar = True
                break

        if not found_similar:
            result_list.append(topic)

    return result_list



def is_similar(t1, t2, limit):
    matcher = SequenceMatcher(None, t1.lower().strip(), t2.lower().strip())
    return matcher.ratio() >= limit


def match_to_existing(topic_name, existing_topics, limit):
    if not existing_topics:
        return topic_name
    
    for topic in existing_topics:
        if is_similar(topic_name, topic, limit):
            topic_name = topic
            break
    return topic_name
