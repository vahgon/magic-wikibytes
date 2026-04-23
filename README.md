# magic-wikibytes

An application that parses the wikitable located at Wikipedia's [List of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures) into json and markdown

## How it Works

_magic-wikibytes_ will make at most two GET requests to the Wikimedia API. The first request calls for the revision id of the Wikipedia page [List of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures). The second request asks for the page content. This request is conditional—If the revision id is not identical to the revision id of the application's last execution (or if `--force` is specified), the request is made.

Because differing authors can contribute to the Wikitable, the format of each cell can differ compared to another. As such, many checks are performed during the parsing process. During this process, the user can provide command-line arguments to alter the final format of the parsed table.

Example outputs of this application can be seen at this project's [docs directory](https://github.com/vahgon/magic-wikibytes/tree/main/docs).

## Getting Started

1. Clone the repo

   ```
   $ git clone https://github.com/vahgon/magic-wikibytes
   ```

2. Install required packages

   ```
   $ pip3 install -r requirements.txt
   ```

After cloning the repo and installing the required packages, run the app
   ```
   $ python3 wikibytes.py
   ```

When ran for the first time, the application will ask for you to input your email address. This is to adhere to the Wikimedia API's [access policy](https://www.mediawiki.org/wiki/Wikimedia_APIs/Access_policy#Client_identification); the given email address is set as the value of all future requests' User-Agent header. This email address is then saved in _./lib/util/.conf_ and can be changed manually by directly editing the value of `EMAIL` in the file, or by specifying a different email before executing the application by use of the `--email` argument.
