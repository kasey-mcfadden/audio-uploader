from internetarchive import upload, get_item
from dotenv import load_dotenv
from urllib.parse import quote
import requests
import os
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
        'description': description
    }

    try:
        response = requests.post(
            'https://archive.org/metadata/items',
            headers={'authorization': 'LOW {}:{}'.format(iaEmail, iaPassword)},
            json=metadata
        )
        response.raise_for_status()
        identifier = response.json()['uniq']
        return identifier
    except requests.exceptions.HTTPError as error:
        print('HTTP error occurred: {}'.format(error))
        return None
    except KeyError as error:
        print('Identifier not found in response: {}'.format(error))
        return None


def upload_item(identifier: str, title: str, file_path: str) -> str:
    """
    Uploads a file to an existing item on the Internet Archive.

    Args:
        identifier (str): The identifier of the item to upload the file to.
        title (str): The title of the file being uploaded.
        file_path (str): The local path to the file to be uploaded.

    Returns:
        str: A URL to the uploaded file on the Internet Archive.

    Raises:
        Exception: If an error occurs while uploading the file.

    Example:
        >>> upload_item('my-item', 'My File.mp3', '/path/to/My File.mp3')
        'https://archive.org/download/my-item/My%20File.mp3'

    """
    try:
        item = get_item(identifier)
        item.upload(file_path, access_key=s3AccessKey, secret_key=s3Secret)
        file_name = os.path.basename(file_path)
        return 'https://archive.org/download/{}/{}'.format(identifier, quote(file_name))
    except Exception as e:
        print('Error uploading item: {}'.format(e))
        return None

def main():
    """
    The main function of the program.
    """
    collection = 'piece_mp3s'
    title = 'Bird in Space'
    description = 'Mp3 audio for {}'.format(title)

    file_path = '/Users/kaseym/Downloads/MP3s'
    file_name = '{}.mp3'.format(title)
    full_path = os.path.join(file_path, file_name)

    identifier = create_item(collection, title, description)
    url = upload_item(identifier, title, full_path)
    print(url)

if __name__ == '__main__':
    main()