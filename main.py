from app.views.main import app
from app.controllers.role import RoleController
from sentry_sdk import capture_exception

if __name__ == "__main__":
    RoleController.check_and_create_roles()
    try:
        app()
    except Exception as e:
        capture_exception(e)