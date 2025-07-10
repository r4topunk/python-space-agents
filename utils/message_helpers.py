def make_log(node: str, status: str, content: str) -> dict:
    # print(f"📝 [SERVER LOG] [{node.upper()}] {status.upper()}: {content}")
    return {
        "type": "LOG",
        "node": node,
        "status": status,
        "content": content,
    }

def make_reply(messages: list) -> dict:
    return {
        "type": "Reply",
        "message": messages
    }

def make_message(content: str) -> dict:
    return {
        "type": "message",
        "content": content
    }

def make_error(error_msg: str) -> dict:
    return {
        "type": "error",
        "error": error_msg
    }

