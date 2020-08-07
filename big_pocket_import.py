#!/usr/bin/python3

import os
import math


def get_list_from_header(rl, heading, end_index):
    start_index = 0
    for index, line in enumerate(rl):
        if f"<h1>{heading}</h1>" in line.strip():
            print(f"found heading {line.strip()} at index {index}")
            start_index = index
            break
    list_items = rl[start_index: end_index]
    return (start_index,
            [list_item.strip()
             for list_item in list_items if "<li><a href" in list_item])


def get_reading_lists(rl):
    archive_index, archive = get_list_from_header(
        rl, "Read Archive", len(rl))
    unread_index, unread = get_list_from_header(rl, "Unread", archive_index-1)
    return [unread, archive]


def chunks(items, chunk_size):
    for index in range(0, len(items), chunk_size):
        yield items[index:index + chunk_size]


def max_row_for_mb(byte_size, rows):
    human_readable = byte_size / (1024 * 1024)  # MB
    divisible_to_mb = math.ceil(human_readable)
    max_row = int(len(rows) / divisible_to_mb)
    return max_row


def split_lists_to_MB_chunks(max_row, rlists):
    return [list(chunks(rl, max_row)) for rl in rlists]


def write_pocket_exports(rl_chunks):
    chunk_size = max([len(rlc) for rlc in rl_chunks])
    [unread_chunks, archive_chunks] = rl_chunks

    template = """
    <!DOCTYPE html>
    <html>
        <!--So long and thanks for all the fish-->
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Pocket Export</title>
        </head>
        <body>
            <h1>Unread</h1>
            <ul>
            {}
            </ul>

            <h1>Read Archive</h1>
            <ul>
            {}
            </ul>
        </body>
    </html>
    """

    for index in range(0, chunk_size):
        with open(f'{index}.html', "w+") as f:
            unread_chunk = unread_chunks[index] if unread_chunks[index:] else ''
            archive_chunk = archive_chunks[index] if archive_chunks[index:] else ''
            f.writelines(
                template.format(
                    '\n'.join(unread_chunk),
                    '\n'.join(archive_chunk)
                )
            )


def main():
    filename = "ril_export.html"
    byte_size = os.stat(filename).st_size
    with open(filename) as f:
        rl = f.readlines()
    rlists = get_reading_lists(rl)
    max_row = max_row_for_mb(byte_size, rl)
    rl_chunks = split_lists_to_MB_chunks(max_row, rlists)
    write_pocket_exports(rl_chunks)


if __name__ == "__main__":
    main()
