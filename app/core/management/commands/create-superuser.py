"""
    Command created by c00kiemon5ter at:
    https://gist.github.com/c00kiemon5ter/7806c1eac8c6a3e82f061ec32a55c702
"""

from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = 'Create a superuser with a password non-interactively'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--email', dest='email', default=None,
            help='Specifies the email for the superuser.',
        )
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        database = options.get('database')
        password = options.get('password')
        username = options.get('username')
        email = options.get('email')

        if not password or not username or not email:
            raise CommandError(
                    "--email --username and --password are required options")

        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }

        self.UserModel._default_manager.db_manager(
                database).create_superuser(**user_data)

        if options.get('verbosity', 0) >= 1:
            self.stdout.write("Superuser created successfully.")