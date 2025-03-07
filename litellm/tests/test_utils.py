import sys, os
import traceback
from dotenv import load_dotenv

load_dotenv()
import os

sys.path.insert(
    0, os.path.abspath("../..")
)  # Adds the parent directory to the system path
import pytest
import litellm
from litellm.utils import trim_messages, get_token_count

# Assuming your trim_messages, shorten_message_to_fit_limit, and get_token_count functions are all in a module named 'message_utils'

# Test 1: Check trimming of normal message
def test_basic_trimming():
    messages = [{"role": "user", "content": "This is a long message that definitely exceeds the token limit."}]
    trimmed_messages = trim_messages(messages, model="claude-2", max_tokens=8)
    print("trimmed messages")
    print(trimmed_messages)
    # print(get_token_count(messages=trimmed_messages, model="claude-2"))
    assert (get_token_count(messages=trimmed_messages, model="claude-2")) <= 8
test_basic_trimming()

def test_basic_trimming_no_max_tokens_specified():
    messages = [{"role": "user", "content": "This is a long message that is definitely under the token limit."}]
    trimmed_messages = trim_messages(messages, model="gpt-4")
    print("trimmed messages for gpt-4")
    print(trimmed_messages)
    # print(get_token_count(messages=trimmed_messages, model="claude-2"))
    assert (get_token_count(messages=trimmed_messages, model="gpt-4")) <= litellm.model_cost['gpt-4']['max_tokens']
test_basic_trimming_no_max_tokens_specified()

def test_multiple_messages_trimming():
    messages = [
        {"role": "user", "content": "This is a long message that will exceed the token limit."},
        {"role": "user", "content": "This is another long message that will also exceed the limit."}
    ]
    trimmed_messages = trim_messages(messages=messages, model="gpt-3.5-turbo", max_tokens=20)
    print("Trimmed messages")
    print(trimmed_messages)
    # print(get_token_count(messages=trimmed_messages, model="gpt-3.5-turbo"))
    assert(get_token_count(messages=trimmed_messages, model="gpt-3.5-turbo")) <= 20
test_multiple_messages_trimming()

def test_multiple_messages_no_trimming():
    messages = [
        {"role": "user", "content": "This is a long message that will exceed the token limit."},
        {"role": "user", "content": "This is another long message that will also exceed the limit."}
    ]
    trimmed_messages = trim_messages(messages=messages, model="gpt-3.5-turbo", max_tokens=100)
    print("Trimmed messages")
    print(trimmed_messages)
    assert(messages==trimmed_messages)

test_multiple_messages_no_trimming()


def test_large_trimming():
    messages = [{"role": "user", "content": "This is a singlelongwordthatexceedsthelimit."}, {"role": "user", "content": "This is a singlelongwordthatexceedsthelimit."},{"role": "user", "content": "This is a singlelongwordthatexceedsthelimit."},{"role": "user", "content": "This is a singlelongwordthatexceedsthelimit."},{"role": "user", "content": "This is a singlelongwordthatexceedsthelimit."}]
    trimmed_messages = trim_messages(messages, max_tokens=20, model="random")
    print("trimmed messages")
    print(trimmed_messages)
    assert(get_token_count(messages=trimmed_messages, model="random")) <= 20
test_large_trimming()