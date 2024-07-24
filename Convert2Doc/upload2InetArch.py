from internetarchive import get_item, Item

def upload_to_internet_archive(identifier, files, access_key, secret_key, metadata):
    """
    Uploads files to the Internet Archive.

    Args:
    identifier (str): Unique identifier for the item on the Internet Archive.
    files (list of str): List of filenames to be uploaded.
    access_key (str): Your Internet Archive access key.
    secret_key (str): Your Internet Archive secret key.
    metadata (dict): Metadata for the item being uploaded.

    Returns:
    int: HTTP status code of the upload request or None if an error occurred.
    """
    try:
        item = Item(identifier)
        response = item.upload(files=files, metadata=metadata, access_key=access_key, secret_key=secret_key)
        return response[0].status_code
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
