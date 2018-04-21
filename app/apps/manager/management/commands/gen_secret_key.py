import requests
import logging
from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.hashers import make_password, check_password

logger = logging.getLogger('default')

class Command(BaseCommand):
    help = 'Generates a hash to use as the secret key based on the given string.'

    def add_arguments(self, parser):
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        password = options['password']
        hash_pass = make_password(password)
        logger.info("Hashed password: \n{0}".format(hash_pass))
