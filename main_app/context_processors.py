from .models import Profile

def profile_exists(request):
    logged_in_profile = False

    if request.user.is_authenticated:
        try:
            Profile.objects.get(user=request.user)
            logged_in_profile = True
        except Profile.DoesNotExist:
            pass

    return {'logged_in_profile': logged_in_profile}