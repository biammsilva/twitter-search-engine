import os
import re
from urllib import parse
from typing import List
from collections import Counter

from requests import get, Response
import typer
from dotenv import load_dotenv


application = typer.Typer()


@application.command()
def get_top_100(term: str, language: str = '') -> None:
    if not os.environ.get('TWITTER_BEARER_TOKEN'):
        typer.echo(
            'You need to set the environment variable: "TWITTER_BEARER_TOKEN"'
        )
        return None
    response = get_twitter_top_100({
        'q': term,
        'result_type': 'popular',
        'count': 100,
        'lang': language
    })
    if response.ok:
        data = response.json()
        hashtags = []
        count = 0
        typer.echo('** Top 100 Tweets **\n')
        while count < 100:
            for status in data['statuses']:
                count += 1
                typer.echo('Tweet {}: {}\n'.format(count, status['text']))
                hashtags.extend(find_hashtag(status['text']))
                if count == 100:
                    break
            next_page = data['search_metadata']['next_results']
            params_next_page = get_url_params(next_page)
            get_twitter_top_100(params_next_page)
            data = response.json()
        hashtags_ranking = Counter(hashtags)
        typer.echo('\n** Top Hashtags **\n')
        count = 0
        for hashtag, ocurrences in hashtags_ranking.most_common(10):
            count += 1
            typer.echo('{} - hashtag: #{}, ocurrences: {}'
                       .format(count, hashtag, ocurrences))
    else:
        typer.echo('Api call failed. Reason:')
        typer.echo(response.json())


def find_hashtag(tweet: str) -> List[str]:
    return re.findall(r"#(\w+)", tweet)


def get_url_params(querystring: str) -> dict:
    return parse.parse_qs(querystring)


def get_twitter_top_100(params: dict) -> Response:
    return get(
        'https://api.twitter.com/1.1/search/tweets.json',
        params=params,
        headers={
            'Authorization': 'Bearer {}'.format(
                os.environ['TWITTER_BEARER_TOKEN']
            )
        }
    )


if __name__ == "__main__":
    load_dotenv()
    application()
