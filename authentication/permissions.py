from rest_framework import permissions

SISAGEN_ROLES = [
    "Sisagen_Admin",
    "Sisagen_DataManager",
    "Sisagen_Paziente",
    "Sisagen_ResponsabileStruttura",
    "Sisagen_Specialista"
    ]

class SisagenPermission(permissions.BasePermission):
    """
    Global permission check for Sisagen-affiliated users.
    """

    def has_permission(self, request, view):

        user_groups = request.user.groups
        # Sisagen roles held by user
        user_SGgroups = [role["name"] for role in user_groups if role["name"] in SISAGEN_ROLES]

        # deny if user is not Sisagen
        if not user_SGgroups:
            return False
        
        # always allow for read-only methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # deny if user only has Sisagen_Paziente
        return not user_SGgroups == ["Sisagen_Paziente"]