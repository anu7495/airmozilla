from django.core.management.base import BaseCommand


class Command(BaseCommand):  # pragma: no cover
    """We USED to have djcelery installed but it was an ancient version.
    And we never used it. Because those tables lingering, we can't execute
    `./manage.py syncdb` and `./manage.py migrate`

    There's no harm in deleting these tables because the worst thing
    that can happen is that we lose some pending jobs.
    However, at the time of writing we don't have a message queue working.
    """
    def handle(self, *args, **options):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
        DROP TABLE  celery_taskmeta;
        DROP TABLE  celery_tasksetmeta;
        DROP TABLE  djkombu_message;
        DROP TABLE  djkombu_queue;
        DROP TABLE  djcelery_taskstate;
        DROP TABLE  djcelery_workerstate;
        DROP TABLE  djcelery_periodictasks;
        DROP TABLE  djcelery_periodictask;
        DROP TABLE  djcelery_intervalschedule;
        DROP TABLE  djcelery_crontabschedule;

        DELETE FROM south_migrationhistory WHERE app_name = 'djcelery';
        DELETE FROM south_migrationhistory WHERE app_name = 'django';
        """)
        connection.commit()
