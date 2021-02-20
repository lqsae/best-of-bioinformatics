from requests_html import HTMLSession


def get_stars(url):
    stars = set()
    session = HTMLSession()
    r = session.get(url)
    for href in r.html.xpath("//div[@class='d-inline-block mb-1']/h3/a/@href"):
        repo = href.replace("/", "", 1).strip().lower()
        stars.add(repo)
    next_urls = r.html.xpath(
        "//a[@class='btn btn-outline BtnGroup-item']/@href")
    next_flags = r.html.xpath(
        "//a[@class='btn btn-outline BtnGroup-item']/text()")
    if "Next" in next_flags:
        next_url = next_urls[-1]
    else:
        next_url = None
    return stars, next_url


in_yaml = set()
with open("projects.yaml", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("github_id"):
            github_id = line.replace("github_id:", "").strip().lower()
            in_yaml.add(github_id)

in_github = set()
url = "https://github.com/xhqsm?tab=stars"
while url:
    stars, url = get_stars(url)
    in_github.update(stars)
in_github.remove("xhqsm/best-of-bioinformatics")

print(in_github - in_yaml)
print(in_yaml - in_github)
