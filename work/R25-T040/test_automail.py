"""Tests and mutation-resistance proofs for automail.py – R25-T040.

Preconditions & source line citations (based on automail.py baseline):
  - Line 11: recThreads is an iterable of thread objects, each exposing .messages[0]
  - Line 14: messages[0].subject is a space-separated string (split(" "))
  - Line 15: messages[0].sender contains an email address matching r"<(.*)@(.*)>"
  - Line 16: Command trigger condition: subEval[0] == "Simon" and subEval[1] == "says:"
  - Line 23: replyContent accumulation: "I am now doing " + " ".join(subEval)
  - Line 24: client.send(replyAddress, replyContent, replyContent) sends response
  - Line 25: client._trash(thread) trashes processed thread
  - Line 26: Remote kill command: subEval[0] == "ENDTASK" terminates loop
"""
import copy
import re
from pathlib import Path
import pytest

import automail

# ---------------------------------------------------------------------------
# Test Fixtures / Stubs
# ---------------------------------------------------------------------------
class MockMessage:
    def __init__(self, subject: str, sender: str):
        self.subject = subject
        self.sender = sender


class MockThread:
    def __init__(self, subject: str, sender: str):
        self.messages = [MockMessage(subject, sender)]


class MockGmailClient:
    def __init__(self):
        self.sent = []
        self.trashed = []

    def send(self, recipient: str, subject: str, body: str):
        self.sent.append({"recipient": recipient, "subject": subject, "body": body})

    def _trash(self, thread: MockThread):
        self.trashed.append(thread)


# ---------------------------------------------------------------------------
# Plausible One-Line Mutant Implementations (used exclusively for proof)
# ---------------------------------------------------------------------------
def automail_mutant_accumulation(recThreads=None, client=None, single_pass=True):
    """Mutant 1: Plausible mistake in line 23 accumulation: missing trailing space.
    Mutated line:
        replyContent = "I am now doing" + " ".join(subEval)
    instead of:
        replyContent = "I am now doing " + " ".join(subEval)
    """
    findEmail = re.compile(r"<(.*)@(.*)>")
    actions = []
    threads = recThreads or []
    i = 0
    for msg in threads:
        subEval = threads[i].messages[0].subject.split(" ")
        sender = threads[i].messages[0].sender
        if len(subEval) >= 2 and subEval[0] == "Simon" and subEval[1] == "says:":
            subEval.remove("Simon")
            subEval.remove("says:")
            match = findEmail.search(sender)
            replyAddress = match.group(0).replace("<", "").replace(">", "") if match else sender
            # MUTANT LINE: missing space after 'doing'
            replyContent = "I am now doing" + " ".join(subEval)
            if client:
                client.send(replyAddress, replyContent, replyContent)
                client._trash(threads[i])
            actions.append({"recipient": replyAddress, "subject": replyContent, "body": replyContent})
        i += 1
    return actions


def automail_mutant_boundary(recThreads=None, client=None, single_pass=True):
    """Mutant 2: Off-by-one boundary check in line 16.
    Mutated condition:
        len(subEval) > 2  (rejects smallest valid input where len == 2)
    instead of:
        len(subEval) >= 2
    """
    findEmail = re.compile(r"<(.*)@(.*)>")
    actions = []
    threads = recThreads or []
    i = 0
    for msg in threads:
        subEval = threads[i].messages[0].subject.split(" ")
        sender = threads[i].messages[0].sender
        # MUTANT LINE: strict > 2 skips empty command body (smallest valid input)
        if len(subEval) > 2 and subEval[0] == "Simon" and subEval[1] == "says:":
            subEval.remove("Simon")
            subEval.remove("says:")
            match = findEmail.search(sender)
            replyAddress = match.group(0).replace("<", "").replace(">", "") if match else sender
            replyContent = "I am now doing " + " ".join(subEval)
            if client:
                client.send(replyAddress, replyContent, replyContent)
                client._trash(threads[i])
            actions.append({"recipient": replyAddress, "subject": replyContent, "body": replyContent})
        i += 1
    return actions


# ===========================================================================
# 1. TestSmallestValidInput & TestOrdinaryInput
# ===========================================================================
class TestSmallestValidInput:
    """Fixture 1: Smallest valid input for automail.
    Subject: 'Simon says:' (exactly 2 tokens, smallest trigger)
    Sender: 'User <u@domain.org>'
    Precondition source lines: 11, 14, 15, 16, 23, 24, 25.
    """

    def test_smallest_valid_input_response(self):
        client = MockGmailClient()
        threads = [MockThread("Simon says:", "User <u@domain.org>")]

        actions = automail.automail(recThreads=threads, client=client, single_pass=True)

        # Explicit expected values
        expected_recipient = "u@domain.org"
        expected_subject = "I am now doing "
        expected_body = "I am now doing "

        assert len(actions) == 1
        assert actions[0]["recipient"] == expected_recipient
        assert actions[0]["subject"] == expected_subject
        assert actions[0]["body"] == expected_body

        # Verify client calls
        assert len(client.sent) == 1
        assert client.sent[0]["recipient"] == expected_recipient
        assert client.sent[0]["subject"] == expected_subject
        assert len(client.trashed) == 1
        assert client.trashed[0] == threads[0]


class TestOrdinaryInput:
    """Fixture 2: Ordinary input for automail.
    Subject: 'Simon says: check server status'
    Sender: 'Admin Staff <admin@corp.net>'
    Precondition source lines: 11, 14, 15, 16, 23, 24, 25.
    """

    def test_ordinary_input_response(self):
        client = MockGmailClient()
        threads = [MockThread("Simon says: check server status", "Admin Staff <admin@corp.net>")]

        actions = automail.automail(recThreads=threads, client=client, single_pass=True)

        expected_recipient = "admin@corp.net"
        expected_subject = "I am now doing check server status"
        expected_body = "I am now doing check server status"

        assert len(actions) == 1
        assert actions[0]["recipient"] == expected_recipient
        assert actions[0]["subject"] == expected_subject
        assert actions[0]["body"] == expected_body

        assert len(client.sent) == 1
        assert client.sent[0]["recipient"] == expected_recipient
        assert client.sent[0]["subject"] == expected_subject
        assert len(client.trashed) == 1


# ===========================================================================
# 2. Mutation Resistance: Original Passes, Mutant Fails Same Named Assertion
# ===========================================================================
class TestMutationResistance:
    """Proves that a regression test detects plausible one-line mistakes."""

    def test_accumulation_invariant_ordinary_input(self):
        """Assertion named 'test_accumulation_invariant_ordinary_input':
        Protects the space separation in: 'I am now doing ' + ' '.join(subEval).
        Source line: Line 23.
        """
        client = MockGmailClient()
        threads = [MockThread("Simon says: jump", "Alice <alice@test.com>")]

        actions = automail.automail(recThreads=threads, client=client, single_pass=True)

        # The clean implementation passes this assertion
        assert actions[0]["subject"] == "I am now doing jump"

    def test_mutant_fails_accumulation_invariant(self):
        """Proves that automail_mutant_accumulation fails the exact same semantic assertion."""
        client = MockGmailClient()
        threads = [MockThread("Simon says: jump", "Alice <alice@test.com>")]

        actions_mutant = automail_mutant_accumulation(recThreads=threads, client=client, single_pass=True)

        # Mutant produces 'I am now doingjump' instead of 'I am now doing jump'
        with pytest.raises(AssertionError):
            assert actions_mutant[0]["subject"] == "I am now doing jump"

    def test_boundary_invariant_smallest_input(self):
        """Protects boundary condition: len(subEval) >= 2 supports 'Simon says:'.
        Source line: Line 16.
        """
        client = MockGmailClient()
        threads = [MockThread("Simon says:", "Bob <bob@test.com>")]

        actions = automail.automail(recThreads=threads, client=client, single_pass=True)
        assert len(actions) == 1
        assert actions[0]["subject"] == "I am now doing "

    def test_mutant_fails_boundary_invariant(self):
        """Proves that automail_mutant_boundary fails the exact same semantic assertion."""
        client = MockGmailClient()
        threads = [MockThread("Simon says:", "Bob <bob@test.com>")]

        actions_mutant = automail_mutant_boundary(recThreads=threads, client=client, single_pass=True)

        # Mutant skips smallest valid input because len == 2 is not > 2
        with pytest.raises(AssertionError):
            assert len(actions_mutant) == 1


# ===========================================================================
# 3. Control Commands & Edge Cases
# ===========================================================================
class TestControlCommands:
    """Verifies control commands such as ENDTASK and non-matching emails."""

    def test_endtask_stops_processing(self):
        """Line 26: subEval[0] == 'ENDTASK' terminates processing immediately."""
        client = MockGmailClient()
        threads = [
            MockThread("ENDTASK", "Controller <ctl@system.org>"),
            MockThread("Simon says: should not run", "User <u@domain.org>"),
        ]

        actions = automail.automail(recThreads=threads, client=client, single_pass=True)
        assert len(actions) == 0
        assert len(client.sent) == 0

    def test_ignore_unrelated_subjects(self):
        """Emails without 'Simon says:' trigger are ignored and untrashed."""
        client = MockGmailClient()
        threads = [MockThread("Hello World", "Friend <friend@chat.com>")]

        actions = automail.automail(recThreads=threads, client=client, single_pass=True)
        assert len(actions) == 0
        assert len(client.sent) == 0
        assert len(client.trashed) == 0
