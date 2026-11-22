# find documentation for ezgmail module at https://pypi.org/project/EZGmail/
# simple simon says module that interacts with google API to read the subject line of an email and respond to "Simon says:"
# DO NOT FORGET TO ADD CREDENTIALS.JSON AND TOKEN.JSON TO .GITIGNORE!!!

import re
import time

try:
    import ezgmail
except ImportError:
    ezgmail = None


def automail(recThreads=None, client=None, single_pass=True):
    """
    Process incoming email threads, responding to 'Simon says:' commands and handling 'ENDTASK'.

    Preconditions (source citations from automail.py baseline):
      - Line 11: recThreads is an iterable of thread objects, each having .messages[0]
      - Line 14: messages[0].subject is a space-separated string (split(" "))
      - Line 15: messages[0].sender contains an email address in '<user@domain>' format
      - Line 16: Command trigger checks subEval[0] == "Simon" and subEval[1] == "says:"
      - Line 23: replyContent accumulation: "I am now doing " + " ".join(subEval)
      - Line 24: client.send(replyAddress, replyContent, replyContent) sends response
      - Line 25: client._trash(recThreads[i]) moves thread to trash
      - Line 26: Remote kill command: subEval[0] == "ENDTASK" terminates loop

    Args:
        recThreads: Optional list of thread objects. If None, queries client.recent().
        client: Gmail client module or mock (default: ezgmail).
        single_pass: If True, processes one batch and returns. If False, runs indefinitely.

    Returns:
        list of dict: Each entry represents a sent reply:
            {"recipient": replyAddress, "subject": replyContent, "body": replyContent}
    """
    if client is None:
        client = ezgmail

    findEmail = re.compile(r"<(.*)@(.*)>")
    actions = []
    check = True

    while check:
        threads = recThreads if recThreads is not None else (client.recent() if client else [])
        i = 0
        for msg in threads:
            if not threads[i].messages:
                i += 1
                continue
            subEval = threads[i].messages[0].subject.split(" ")
            sender = threads[i].messages[0].sender

            if len(subEval) >= 2 and subEval[0] == "Simon" and subEval[1] == "says:":
                subEval.remove("Simon")
                subEval.remove("says:")
                match = findEmail.search(sender)
                replyAddress = (
                    match.group(0).replace("<", "").replace(">", "")
                    if match
                    else sender
                )
                replyContent = "I am now doing " + " ".join(subEval)
                if client:
                    client.send(replyAddress, replyContent, replyContent)
                    client._trash(threads[i])
                actions.append(
                    {
                        "recipient": replyAddress,
                        "subject": replyContent,
                        "body": replyContent,
                    }
                )

            if len(subEval) >= 1 and subEval[0] == "ENDTASK":  # remote kill command
                check = False
                break
            i += 1

        if single_pass:
            break
        time.sleep(60)

    return actions


if __name__ == "__main__":
    automail(single_pass=False)
