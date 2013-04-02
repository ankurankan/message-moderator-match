from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from models import Report,UserProfile,Tag
from django.contrib.auth.models import User

admin.site.register(Report)
admin.site.register(Tag)

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
