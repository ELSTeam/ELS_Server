import firebase_admin
from firebase_admin import credentials
from google.cloud import storage
import datetime


class Firebase:
    def __init__(self) -> None:
        try:
            self.cred = credentials.Certificate('firebase_creds.json')
            firebase_admin.initialize_app(self.cred)
            self.bucket_name = "elderly-life-savior.appspot.com"
        except ConnectionRefusedError as e:
            print(e)
            print("No file found")
        except FileNotFoundError as e:
            print(e)
            print("No file found")

    def upload_file_to_storage(self, local_file_path:str, destination_blob_name) -> bool:
        try:
            """Uploads a local file to the specified bucket in Firebase Storage."""
            # Create a client to interact with the storage service.
            storage_client = storage.Client()

            # Specify the bucket where the file will be uploaded.
            bucket = storage_client.bucket(self.bucket_name)
            # Upload the local file to the destination in Firebase Storage.
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(local_file_path)
            return True
        except Exception as e:
            print(e)
            return False
    
    def get_file_from_storage(self,file_name:str) -> str:
        """Gets the download URL of a file from Firebase Storage using the filename as a query."""
        # Create a client to interact with the storage service.
        storage_client = storage.Client()
        # Specify the bucket where the file is located.
        bucket = storage_client.bucket(self.bucket_name)

        # Get the blob (file) using the filename as a query.
        blob = bucket.get_blob(file_name)

        if blob is not None:
            # Get the download URL of the blob.
            expiration = datetime.timedelta(minutes=5)  # Set the desired expiration time.
            download_url = blob.generate_signed_url(expiration=expiration)
            return download_url
        else:
            return None


# Example
# fire = Firebase()
# fire.upload_file_to_storage("download.jpeg","name_on_the_firebase_bucket.jpeg") # return True or False
# url = fire.get_file_from_storage("name_on_the_firebase_bucket.jpeg") # return string of the url
# print(url)