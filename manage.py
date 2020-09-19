import csv
import click
import requests


@click.group()
def cmd():
    pass


@cmd.command()
def update_test_html():
    results = []

    with open("test/data/urls/urls.csv", "r") as f:
        reader = csv.DictReader(f)
        for i, x in enumerate(reader):
            res = requests.get(x["url"])
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            results.append((i, res.text))

    for i, html in results:
        with open(f"test/data/htmls/{i}.html", "w") as f:
            f.write(html)


def main():
    cmd()


if __name__ == "__main__":
    main()
