# Twitter search engine

In this cli, you'll be able to get the top 100 tweets by term and get the 10 most common hashtags used in those tweets.

## How to:

### Install:

    virtualenv -p python3
    source env/bin/activate
    pip install -r requirements.txt

### Run:

    python app.py <term>

### Run in another language:

    python app.py <term> --language=<lang>

### Examples:

    python app.py maisa --language=pt

## Data returned:

This cli will return the top 100 tweets for the searched term and the top 10 hashtags used in those tweets.

