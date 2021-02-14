class RequestProcessor:
    def __init__(
        self, upload_signer, download_signer, upload_limit_in_mb, allowed_extension
    ):
        self.upload_signer = upload_signer
        self.download_signer = download_signer
        self.upload_limit_in_mb = upload_limit_in_mb
        self.allowed_extension = allowed_extension

    def process_request(self, request_id, extension):
        if not extension:
            raise ValueError("no extension provided")

        normalised_extension = extension.lower()
        is_image = normalised_extension in self.allowed_extension

        if not is_image:
            raise ValueError(f"extension {extension} is not supported")

        file_key = f"{request_id}.{normalised_extension}"
        return {
            "upload": self.upload_signer.sign_upload(file_key, self.upload_limit_in_mb),
            "download": self.download_signer.sign_download(file_key),
        }
