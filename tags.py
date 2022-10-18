import json
from datetime import datetime

import fire
import requests


def req(owner_and_repo, kind):
    accept_header = "application/vnd.github+json"
    url = f"https://api.github.com/repos/{owner_and_repo}/{kind}"
    res = requests.get(url, headers={"Accept": accept_header})
    return res.json()


def get_commit(owner_and_repo, commit):
    return req(owner_and_repo, f"git/commits/{commit}")


def get_tags_freq(owner_and_repo, version):
    kind = "tags"
    data = req(owner_and_repo, kind + "?per_page=100")
    data = [(x["name"], get_commit(owner_and_repo, x["commit"]["sha"])["author"]["date"]) for x in data if "rc" not in x["name"] and version in x["name"]]
    data = sorted(data, key=lambda tup: tup[1], reverse=True)
    data = [datetime.strptime(x[1], "%Y-%m-%dT%H:%M:%SZ") for x in data]
    total = 0
    for i in range(1, len(data)):
        total += (data[i-1] - data[i]).days
    total = int(total/len(data))
    print(total)


if __name__ == "__main__":
    fire.Fire(get_tags_freq)
