import urllib.parse
import requests
import pandas as pd
from bs4 import BeautifulSoup

doi = "10.1186/s10152-020-0534-x"

bmc_url = f"https://hmr.biomedcentral.com/articles/{doi}/figures/2"

page = requests.get(bmc_url)
soup = BeautifulSoup(page.content, 'html.parser')

image_tag = soup.find("img", {'aria-describedby':"Fig2"})

image_url = f'https:{image_tag["src"]}'
print(image_url)

description_tag = soup.find("div", {'class':"c-article-figure-description"})

title = description_tag.find("i").text + image_url.split(".")[-1]
print(title)

description = description_tag.text
print(description)

base_url = (
            f"https://api.crossref.org/works/{doi}"
        )
response = requests.get(base_url)
result = response.json()


license = result["message"]["license"][0]
license_url = license["URL"]
print( license["start"])
license_date_parts = license["start"]["date-parts"][0]
license_date_parts = [str(i) for i in license_date_parts]
license_date = "-".join(license_date_parts)

author_list = result["message"]["author"]
first_author_name = author_list[0]["given"] + " " + author_list[0]["family"]


switcher = {"https://creativecommons.org/licenses/by/4.0": "cc-by-4.0", "cc-by-sa": "cc-by-sa-4.0", "cc0": "Cc-zero"}

license = switcher[license_url]

summary = """{{Information"""   + f"""
|description={{{{en|{description} (Text in [{license_url} {license}] from [{bmc_url} {first_author_name} et al. ] ) }}}}
|date={license_date}
|source={bmc_url}
|author={first_author_name} et al.
|permission=
|other versions=""" + """
}}
[[Category:Science]]"""

upload_page = "https://commons.wikimedia.org/wiki/Special:Upload"

summary_for_url = urllib.parse.quote(summary)
title_for_url = urllib.parse.quote(title)
upload_url = (
    upload_page
    + f"?wpUploadDescription={summary_for_url}&wpLicense={license}&wpDestFile={title_for_url}&wpSourceType=url&wpUploadFileURL={image_url}"
)

print(upload_url)