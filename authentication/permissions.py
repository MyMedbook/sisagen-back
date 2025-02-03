from rest_framework import permissions

SISAGEN_ROLES = [
    "Sisagen_Admin",
    "Sisagen_ResponsabileStruttura",
    "Sisagen_DataManager",
    "Sisagen_Specialista",
    "Sisagen_Paziente"
    ]

def sisagen_rank(user):

    user_groups = [role["name"] for role in user.groups]
    for role in SISAGEN_ROLES:
        if role in user_groups:
            return role
        
    return False

class SisagenPermission(permissions.BasePermission):
    """
    Global permission check for Sisagen-affiliated users.
    """

    def has_permission(self, request, view):

        # Sisagen roles held by user
        sisagen_role = sisagen_rank(request.user)

        # deny if user is not Sisagen
        if not sisagen_role:
            return False
        
        # always allow for read-only methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # deny if user only has Sisagen_Paziente
        return not sisagen_role == "Sisagen_Paziente"
