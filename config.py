# separator used by search.py, categories.py, ...
SEPARATOR = ";"

LANG            = "en_US" # can be en_US, fr_FR, ...
ANDROID_ID      = "3ACE97CE25DD06D2" # "xxxxxxxxxxxxxxxx"
GOOGLE_LOGIN    = "okmtghij11@gmail.com" # "username@gmail.com"
GOOGLE_PASSWORD = "okada10!"
AUTH_TOKEN      = "_AQQ6X7F9Zyylt_-nUGitGbguEPwzmsflNnaDViKwf0cjyrdZgeQGENOma-7JEniiWUmCw." # "yyyyyyyyy"

# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not updated")

