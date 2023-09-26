from google.cloud import storage
from google.oauth2 import service_account

class GoogleAuthService:

    def __init__(self, service_account_json_path):
        self.service_account_json_path = service_account_json_path
        self.credentials = None
        self.is_authenticated = False

    def authenticate(self):
        if not self.is_authenticated:
            try:
                self.credentials = service_account.Credentials.from_service_account_file(
                    self.service_account_json_path,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                self.is_authenticated = True
            except Exception as e:
                print(f"Xác thực thất bại: {str(e)}")

    def get_authenticated_client(self):
        if not self.is_authenticated:
            self.authenticate()  # Nếu chưa xác thực, thực hiện xác thực trước
        return storage.Client(credentials=self.credentials)
