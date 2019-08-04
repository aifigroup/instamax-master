from project import db
from project.admin.models import Admin


def admin_password_add():
    Admin.query.delete()

    new_admin = Admin(email='accept_me_admin',
                      password='cors@acceptable$#!')

    db.session.add(new_admin)
    db.session.commit()
    return "True"

admin_password_add()