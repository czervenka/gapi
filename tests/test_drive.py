from init import setUp
setUp()

from unittest import TestCase
from unittest.case import SkipTest

from gapi import Api


__author__ = 'krtek'

class Drive(TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            import local_keys
        except ImportError:
            raise SkipTest("Create local_keys.py to run this test (use local_keys-template.py as template).")
        cls.api = Api(['drive'], **local_keys.AUTH)
        cls.file = {
            'content': '"a","b","c"\n1,2,3',
            'title': 'Title 123 42342342342----980903',
            'mime_type': 'text/csv',
        }
        response = cls.api.drive.files.insert(**cls.file)
        cls.file['id'] = response['id']

    @classmethod
    def tearDownClass(cls):
        for item in cls.api.drive.files.list(q='title="%s"' % cls.file['title'], fields='items/id')['items']:
            cls.api.drive.files.delete(item['id'])

    def test_get_the_file(self):
        'get'
        response = self.api.drive.files.get(self.file['id'])
        self.assertEquals(response['title'], self.file['title'], 'Returned file resource has the same title as the created.')

    def test_drive_search_by_title(self):
        'list (q=\'title="some title"\')'
        files = self.api.drive.files.list(q='title="%s"' % self.file['title'])['items']
        self.assertEquals(len(files), 1, "There should be 1 file but list() returned %r files." % len(files))

    def test_drive_list_by_title(self):
        'list'
        files = self.api.drive.files.list()['items']
        self.assertGreater(len(files), 0, "There is one file at least.")

    def test_drive_touch(self):
        'touch'
        id = self.file['id']
        old_file = self.api.drive.files.get(id)
        changed_file = self.api.drive.files.touch(id)
        self.assertGreater(changed_file['modifiedDate'], old_file['modifiedDate'], "Touch changes the file's modifiedDate")

    def test_trash(self):
        'files.trash+untrash'
        id = self.file['id']
        self.api.drive.files.trash(id)
        self.api.drive.files.untrash(id)

    def test_revisions(self):
        'revisions.list'
        id = self.file['id']
        revs_api = self.api.drive.revisions
        revs_api.file_id = id
        try:
            self.assertGreater(len(revs_api.list()['items']), 0)
        finally:
            revs_api.file_id = None

    def test_revisions_empty_file_id(self):
        'revisions.list - ValueError if no file_id is set'
        self.assertRaises(ValueError, self.api.drive.revisions.list)

    def test_changes(self):
        'changes.list'
        changes = self.api.drive.changes.list()['items']
        # TODO: refine
        self.assertGreater(len(changes), 0)

    def test_about(self):
        'about.get'
        # TODO: refine
        self.assertGreater(self.api.drive.about.get(), 0)

    def test_update(self):
        'files.update'
        response = self.api.drive.files.insert('original content', title='GAPI Test update 1', mime='text/csv')
        id = response['id']
        response = self.api.drive.files.update('updated content', title='GAPI Test update 1', mime='text/csv', id=id)
        # TODO: refine
        self.assertEquals(id, response['id'])
        self.api.drive.files.delete(id)

    def test_permissions(self):
        'permissions.list + get'
        perms_api = self.api.drive.permissions
        perms_api.file_id = self.file['id']
        permissions = perms_api.list()
        self.assertGreater(len(permissions['items']), 0)
        #try to get first permission
        perms_api.get(permissions['items'][0]['id'])
