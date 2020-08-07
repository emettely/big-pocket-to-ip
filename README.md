# big-pocket-to-ip

Breakdown Pocket import HTML files to a manageable 1MB size that Instapaper can handle.

## Context

Importing your reading list from Pocket to Instapaper, the automatic import in Instapaper can throw an error - 413: `payload too big`.
This happens if you have too many things in your reading list and the import file is too big.

Instapaper expects a certain elements to exist in the HTML file, so splitting the file using `split -l 5000` doesn't work either.
See [sample file](./sample.html) to see what the Pocket import file looks like.

## How to

1. Export from Pocket - You can get the Pocket export HTML file from clicking through the settings in Pocket.
2. Save the file in the same directory as the `big_pocket_import.py` as `ril_export.html`
3. Run the code `./big_pocket_import.py`. This expects you to have a Python3 executable binary at `usr/bin/python3`.
4. See the html files generate. The files will be named: `[0-9]+.html`
