message = {"generation_result_message": None}

def update_message_state(item):
    global message
    message['generation_result_message'] = item
    return message