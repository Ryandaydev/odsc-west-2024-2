# swcpy software development kit (SDK)
This is the python SDK to to interact with the SportsWorldCentral Football API, which was created for the book [Hands-On APIs for AI and Data Science](https://hands-on-api-book.com).

## Installing swcpy

To install this SDK in your environment, execute the following command:

`pip install swcpy@git+https://github.com/{owner of repo}/portfolio-project#subdirectory=sdk`

## Example Usage

This SDK implements all the endpoints in the SWC API, in addition to providing bulk downloads of the SWC fantasy data in CSV format.

### Example of normal API functions

To call the SDK functions for normal API endpoints, here is an example:

```python
from swcpy import SWCClient
from swcpy import SWCConfig

config = SWCConfig(url="http://127.0.0.1:8000",backoff=False)
client = SWCClient(config)    
leagues_response = client.list_leagues()
print(leagues_response)
```

### Example of bulk data functions

The build data endpoint return a bytes object. Here is an example of saving a file locally from a bulk file endpoint:

```python
import csv
import os
from io import StringIO

config = SWCConfig()
    client = SWCClient(config)    

    """Tests bulk player download through SDK"""
    player_file = client.get_bulk_player_file()


    # Write the file to disk to verify file download
    output_file_path = data_dir + 'players_file.csv'
    with open(output_file_path, 'wb') as f:
        f.write(player_file)
```