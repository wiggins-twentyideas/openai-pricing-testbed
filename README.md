
## Using


# make python virtualenv and install dependencies
```
python3 -m venv ../env-chatgpt3-testbed
source ../env-chatgpt3-testbed/bin/activate
pip install -r requirements.txt
```

# openai api key

save your openap api key to a file named 'openai_api_key'

# run script
```
python testbed.py
```

help will be displayed and will keep a running token count and pricing total:

```
/quit
/reset - resets session and usage counters
/system <message> - appends a system message
/messages - prints session messages
/responses - prints session responses
/save <filename.json> - dump session to json file
/help



($0.000000) (messages:0) (completion_tokens:0) (prompt_tokens:0) (total_tokens:0)
?>
```