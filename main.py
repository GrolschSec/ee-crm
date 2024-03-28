from app.views.main import app
from app.controllers.role import RoleController

if __name__ == "__main__":
    RoleController.check_and_create_roles()
    app()
