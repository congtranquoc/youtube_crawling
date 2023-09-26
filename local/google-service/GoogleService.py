from google.cloud import storage
from GoogleAuthService import GoogleAuthService

class GoogleService:

    def __init__(self, project_id, bucket_name, service_account_json_path):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.auth_service = GoogleAuthService(service_account_json_path)
        self.client = self.auth_service.get_authenticated_client()
        self.bucket = self.client.bucket(bucket_name)

    def list_files(self, prefix=''):
        """Liệt kê tất cả các tệp trong bucket với tiền tố được chỉ định."""
        blobs = self.bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    def download_file(self, source_blob_name, destination_file_name):
        """Tải tệp từ bucket về máy cục bộ."""
        try:
            blob = self.bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
            print(f"Tải tệp {source_blob_name} thành công!")
            return True  # Trả về True nếu không có lỗi xảy ra
        except Exception as e:
            print(f"Lỗi khi tải tệp {source_blob_name}: {str(e)}")
            return False  # Trả về False nếu có lỗi xảy ra

    def upload_file(self, source_file_name, destination_blob_name):
        """Tải tệp từ máy cục bộ lên bucket."""
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        return f"Tải tệp {destination_blob_name} thành công!"

    def delete_file(self, blob_name):
        """Xóa tệp từ bucket."""
        blob = self.bucket.blob(blob_name)
        blob.delete()
        return f"Xóa tệp {blob_name} thành công!"
