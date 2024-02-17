# Download Documents from DocumentCloud

### Some boring mumbo jumbo:

I don't know what to name or call this, but here is my janky Python3 script to hopefully be useful to someone. This script uses the API on DocumentCloud to download documents based on searches and various other options including filtering by title and organizations. I don't know why, but I ran into a problem where I would get a 429 error and I concluded that it is due to the Access Token not being properly refreshed after about 5 minutes (This is the closest conclusion I got to after dealing with this till 4 AM). As far as I can tell, the wrapper wasn't doing this properly and since I hate python so much I can't be arsed to even try to be 100% sure about this.

Since I hate python so much, some of my code is terrible, but I really don't care. It works and I'm not changing how I run things. I do plan on adding the ability to specify a YAML file with various configuration options which would allow more flexibility in how the files are handled.

---

#### Installation... I guess?

I went with venv over poetry or whatever so to setup the venv environment I just kept things simple and ran: `python3 -m venv venv`

To install venv with debian based systems you just run: `sudo apt-get install python3-venv`

The python packages you do need to install are:

- documentcloud
- multiprocessing
- uuid
- argparse

To install them I just did: `venv/bin/pip3 install documentcloud multiprocessing uuid argparse`

------

#### Usage:

Before doing anything else you should sign up to DocumentCloud via Muckrock which can be done by going to https://www.documentcloud.org/home and hitting signup. Once you signed up just replace the line: `client = DocumentCloud("USERNAME", "PASSWORD")` with your username and password. Your username that you used to sign up goes where `"USERNAME"` is in between the double quotes and your password goes where `"PASSWORD"` is in between the double quotes.

After that you should be able to start using the API via this script.

To read the help message just run: `venv/bin/python3 main.py -h`

The output should be:

```bash
usage: main.py [-h] [--organizations ORGANIZATIONS]
               [--org-file ORG_FILE] [--search SEARCH]
               [--search-file SEARCH_FILE]
               [--filter-title FILTER_TITLE]
               [--title-file TITLE_FILE] [--output OUTPUT]

Simple python3 program to search and download documents from
DocumentCloud.

options:
  -h, --help            show this help message and exit
  --organizations ORGANIZATIONS, -o ORGANIZATIONS
                        Specify an organization(s) to filter
                        and narrow down documents that should
                        be downloaded.
  --org-file ORG_FILE, -of ORG_FILE
                        File with a list of organizations to
                        check for.
  --search SEARCH, -s SEARCH
                        Keyword(s) to search for documents on
                        DocumentCloud.
  --search-file SEARCH_FILE, -sf SEARCH_FILE
                        File containing keywords to search for
                        documents on DocumentCloud.
  --filter-title FILTER_TITLE, -ft FILTER_TITLE
                        Keyword(s) to filter based on title.
  --title-file TITLE_FILE, -tf TITLE_FILE
                        File containing Keyword(s) to filter
                        based on title.
  --output OUTPUT, -od OUTPUT
                        Directory where to save the results
                        to.
```

You could just use the flags and specify everything and use commas to seperate them, but I recommend using files with the various keywords and specify via the flags such as: `venv/bin/python3 main.py -od "Koch" -sf search_test.txt -of orgs.txt -tf titles.txt`

It is a lot better especially if you are adding various different pieces of info such as orgs you want to filter by (e.g. DeSmog, ProPublica, OpenSecrets, etc.) or if you want to filter by titles which lets you only download the files with those titles. This was incorporated due to noticing that even though the search was something else entirely, documents that weren't really related were being downloaded so it kind of didn't filter the way I wanted to. The problem I did ran into with specifying everything via cli is that I had to enclose anything with spaces in double quotes which becomes cumbersome and I rather just put everything into files so it is just less of an annoyance especially if automating ;).

The output is to what directory you want to save to and if not specified would save to the current directory. The titles work in a way where it takes whatever is in there and it loops through what was in the file and replaces the spaces with `-` which was due to noticing that some files had dashes while others had spaces so to make sure all the documents were downloaded properly that matched the keywords for the titles.

It does work in a way where you can omit flags you don't want/need and most are just there for more flexibility and organization.