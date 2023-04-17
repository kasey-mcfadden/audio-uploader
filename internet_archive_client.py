from internetarchive import upload, get_item, get_session, search_items, get_user_info
from dotenv import load_dotenv
from urllib.parse import quote
import requests
import os
from io import BytesIO
load_dotenv()

iaEmail = os.environ.get('IA_EMAIL')
iaPassword = os.environ.get('IA_PASSWORD')
s3AccessKey = os.environ.get('S3_ACCESS_KEY')
s3Secret = os.environ.get('S3_SECRET')

def create_item(collection: str, title: str, description: str) -> str:
    """
    Creates a new item in the Internet Archive with the specified metadata.

    Args:
        collection (str): The name of the collection to add the item to.
        title (str): The title of the item.
        description (str): A brief description of the item.

    Returns:
        str: The identifier of the newly created item.

    Raises:
        requests.exceptions.HTTPError: If the API returns a non-200 status code.
        KeyError: If the identifier is not found in the API response.

    Example:
        >>> create_item('test_collection', 'My Item', 'This is a test item.')
        'my-item'

    """
    metadata = {
        'collection': collection,
        'title': title,
        'description': description,
        'contributor': iaEmail
    }

    try:
        response = requests.post(
            'https://archive.org/metadata/items',
            headers={'authorization': 'LOW {}:{}'.format(iaEmail, iaPassword)},
            json=metadata
        )
        response.raise_for_status()
        identifier = response.json()['uniq']
        print('Item created with identifier: {}'.format(identifier))
        return identifier
    except requests.exceptions.HTTPError as error:
        print('HTTP error occurred: {}'.format(error))
        return None
    except KeyError as error:
        print('Identifier not found in response: {}'.format(error))
        return None


def upload_file(identifier: str, file_bytes: BytesIO) -> str:
    """
    Uploads a file to an existing item on the Internet Archive.

    Args:
        identifier (str): The identifier of the item to upload the file to.
        file_bytes (BytesIO): The BytesIO object of the file to be uploaded.

    Returns:
        str: A URL to the uploaded file on the Internet Archive.

    Raises:
        Exception: If an error occurs while uploading the file.

    Example:
        >>> upload_file('my-item', 'My File.mp3', '/path/to/My File.mp3')
        'https://archive.org/download/my-item/My%20File.mp3'

    """
    try:
        item = get_item(identifier)
        item.upload(file_bytes, access_key=s3AccessKey, secret_key=s3Secret)
        file_name = file_bytes.name
        result_url = 'https://archive.org/download/{}/{}'.format(identifier, quote(file_name))
        print('File uploaded with URL: {}'.format(result_url))
        return result_url
    except Exception as e:
        print('Error uploading item: {}'.format(e))
        return None


import requests
from urllib.parse import quote

def delete_file(identifier: str, file_name: str) -> bool:
    """
    Deletes a file from an existing item on the Internet Archive.

    Args:
        identifier (str): The identifier of the item from which to delete the file.
        file_name (str): The name of the file to be deleted.

    Returns:
        bool: True if the file was successfully deleted, False otherwise.

    Raises:
        Exception: If an error occurs while deleting the file.

    Example:
        >>> delete_file('my-item', 'My File.mp3')
        True

    """
    try:
        base_url = f'https://s3.us.archive.org/{identifier}/{quote(file_name)}'

        headers = {
            'Authorization': f'LOW {s3AccessKey}:{s3Secret}',
        }

        response = requests.delete(base_url, headers=headers)

        if response.status_code == 204:
            print(f'File {file_name} deleted successfully.')
            return True
        else:
            print(f'Error deleting file: {response.text}')
            return False
    except Exception as e:
        print(f'Error deleting file: {e}')
        return False



def get_all_mp3_files() -> list:
    """
    Retrieves all items associated with the user's email and filters the files to only include those with an '.mp3' extension.

    Returns:
        list: A list of dictionaries, each containing the item identifier and the URL of the mp3 file.

    Example:
        >>> get_all_mp3_files()
        [
            {'filename': 'my-file-name', 'identifier': 'my-item', 'url': 'https://archive.org/download/my-item/My%20File.mp3'},
            {'filename': 'another-file-name', 'identifier': 'another-item', 'url': 'https://archive.org/download/another-item/Another%20File.mp3'}
        ]
    """
    mp3_files = []

    # Search for items associated with the user's email
    query = 'uploader:"{}"'.format(iaEmail)
    search_results = search_items(query)

    # Iterate through the items and filter the files with '.mp3' extension
    for item in search_results:
        item_object = get_item(identifier=item.get('identifier'))
       
        item_files = item_object.get_files()
        for file in item_files:
            if file.name.endswith('.mp3'):
                mp3_files.append({
                    'filename': file.name,
                    'identifier': file.identifier,
                    'url': 'https://archive.org/download/{}/{}'.format(file.identifier, quote(file.name))
                })

    return mp3_files


def main():
    """
    The main function of the program.
    """
    create_item('artist_mp3s', 'Artist MP3s', 'These are all the mp3 files for the artist biographies.')
    # mp3_files = get_all_mp3_files()
    # for file in mp3_files:
    #     print(file)

if __name__ == '__main__':
    main()