from os import unlink, path

class LogoutController:
    TOKEN_PATH = path.join(path.expanduser("~"), ".ee_token")

    def __init__(self):
        self.token = None

    def is_token_file_present(self):
        return path.exists(self.TOKEN_PATH)

    def delete_token_file(self):
        try:
            if self.is_token_file_present():
                unlink(self.TOKEN_PATH)
                return [True, None]
            else:
                return [False, "token file not found."]
        except PermissionError:
            return [False, "permission denied."]