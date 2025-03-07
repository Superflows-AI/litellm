# Exception Mapping

LiteLLM maps the 4 most common exceptions across all providers. 
- Rate Limit Errors
- Context Window Errors
- Invalid Request Errors
- InvalidAuth Errors (incorrect key, etc.)

Base case - we return the original exception.

All our exceptions inherit from OpenAI's exception types, so any error-handling you have for that, should work out of the box with LiteLLM. 

For all 4 cases, the exception returned inherits from the original OpenAI Exception but contains 3 additional attributes: 
* status_code - the http status code of the exception
* message - the error message
* llm_provider - the provider raising the exception

## usage

```python 
from litellm import completion

os.environ["ANTHROPIC_API_KEY"] = "bad-key"
try: 
    # some code 
    completion(model="claude-instant-1", messages=[{"role": "user", "content": "Hey, how's it going?"}])
except Exception as e:
    print(e.llm_provider)
```

## details 

To see how it's implemented - [check out the code](https://github.com/BerriAI/litellm/blob/a42c197e5a6de56ea576c73715e6c7c6b19fa249/litellm/utils.py#L1217)

[Create an issue](https://github.com/BerriAI/litellm/issues/new) **or** [make a PR](https://github.com/BerriAI/litellm/pulls) if you want to improve the exception mapping. 

**Note** For OpenAI and Azure we return the original exception (since they're of the OpenAI Error type). But we add the 'llm_provider' attribute to them. [See code](https://github.com/BerriAI/litellm/blob/a42c197e5a6de56ea576c73715e6c7c6b19fa249/litellm/utils.py#L1221)

## custom mapping list

Base case - we return the original exception.

|               | ContextWindowExceededError | AuthenticationError | InvalidRequestError | RateLimitError | ServiceUnavailableError |
|---------------|----------------------------|---------------------|---------------------|---------------|-------------------------|
| Anthropic     | ✅                          | ✅                   | ✅                   | ✅             |                         |
| OpenAI        | ✅                          | ✅                     |✅                     |✅               |✅|
| Replicate     | ✅                          | ✅                   | ✅                   | ✅             | ✅                       |
| Cohere        | ✅                          | ✅                   | ✅                    | ✅             | ✅                        |
| Huggingface   | ✅                          | ✅                   | ✅                   | ✅             |                         |
| Openrouter    | ✅                          | ✅                   | ✅                    | ✅             |                         |
| AI21          | ✅                          | ✅                   | ✅                   | ✅             |                         |
| TogetherAI    | ✅                          | ✅                   | ✅                   | ✅             |                         |
| AlephAlpha    | ✅                          | ✅                   | ✅                   | ✅             | ✅                        |


> For a deeper understanding of these exceptions, you can check out [this](https://github.com/BerriAI/litellm/blob/d7e58d13bf9ba9edbab2ab2f096f3de7547f35fa/litellm/utils.py#L1544) implementation for additional insights.

The `ContextWindowExceededError` is a sub-class of `InvalidRequestError`. It was introduced to provide more granularity for exception-handling scenarios. Please refer to [this issue to learn more](https://github.com/BerriAI/litellm/issues/228).


