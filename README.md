Send firebase message with python
===
## How to get json file

create a project in [firebase console](https://console.firebase.google.com/) and produce a new key in settings->serviceaccounts (select Python).


Setup
===

Put your json file in same folder and set the name of json file as an environment variable of GOOGLE_APPLICATION_CREDENTIALS or set the path of the json file as an environment variable of GOOGLE_APPLICATION_CREDENTIALS.
<br>

run

```
pip install -r requirements.txt
```

Running
===

Put your token in token_list and run

```
python notify.py
```