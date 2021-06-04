from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None):
        if not username:
            raise ValueError('Users must have an username address')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            username=username,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None):

        user = self.create_user(
            username=username,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user
