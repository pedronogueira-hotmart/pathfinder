from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

url = 'http://www.example.com/hithere.2/something/else'


PurePosixPath(
    unquote(
        urlparse(
            url
        ).path
    )
).parts[1]
