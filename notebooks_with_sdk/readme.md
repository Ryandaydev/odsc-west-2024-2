# Using Notebooks with the SDK

These examples use LangChain and LangGraph with the API.

## Some prerequisites

Install the SDK locally from a separate github repo:

    pip3 install swcpy@git+https://github.com/handsonapibook/api-book-part-one#
subdirectory=chapter7/complete/sdk .

Install the requirements for this project:

    pip3 install -r requirements.txt

## Set up an API account with Anthropic
Save the value of the API key somewhere secure.

## Add GitHub Codespaces secrets for these variables

SWC_API_BASE_URL  - put the value your API runs locally, probably http://0.0.0.0:8000 if it's in the Codespace

ANTHROPIC_API_KEY - put the API key from Anthropic in here.
