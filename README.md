# magic-wikibytes

An application that parses the wikitable located at Wikipedia's [List of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures) into json and markdown

## How it Works

_magic-wikibytes_ makes two requests to the Wikimedia API. The first request specifies for only the revision id of the page '[List of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures)' to be sent in the response. This is compared to the revision ID of the app's last execution so as to limit the amount of data sent by the Wikimedia API. If the revision id is not the same as the revision id of the last execution (or if `--force` is specified), a subsequent request is made specifying the page content be in the API response body

Because differing authors can contribute to the Wikitable, the format of each cell can differ compared to another. As such, many checks are performed during the parsing process. During this process, the user can provide command-line arguments to alter the final format of the parsed table.

Example outputs of this application can be seen at this project's [docs directory](https://github.com/vahgon/magic-wikibytes/tree/main/docs).

## Getting Started

1. Clone the repo

   ```
   $ git clone https://github.com/vahgon/magic-wikibytes
   ```

2. Install required packages

   ```
   pip3 install -r requirements.txt
   ```

After cloning the repo and installing the required packages, run the app
   ```
   $ python3 wikibytes.py
   ```

When ran for the first time, the application will ask for your email and save it in _./lib/util/.conf_. This is done to adhere to the Wikimedia API's [access policy](https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy); the provided email address is set as the value for the User-Agent header.
