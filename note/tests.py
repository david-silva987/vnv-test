from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone

from note.models import Note

# Create your tests here.

class NoteTest(TestCase):
    def setUp(self):

        first_note = Note.objects.create(title='first note', content='first content', updated_at=datetime.now())
        second_note = Note.objects.create(title='second note', content='second content', updated_at=datetime.now())
        third_note = Note.objects.create(title='third note', content='third content', updated_at=datetime.now())

    def test_notes_count(self):
        self.assertEqual(Note.objects.count(), 3) #Ensure we have 3 notes

    def test_update_note(self):
        new_title = 'updated title'
        first_note = Note.objects.get(pk=1)
        first_note.title = new_title
        first_note.save()

        self.assertEqual(first_note.title, new_title) #Ensure we have updated the title

    def test_delete_note(self):
        first_note = Note.objects.get(pk=1)
        first_note.delete()
        self.assertEqual(Note.objects.count(), 2) #Ensure we now have 2 notes

    def test_updated_at_note(self):
        now = timezone.now() #to avoid typeError with offset-naive and offset-aware datetimes
        first_note = Note.objects.get(pk=1)
        first_note.updated_at = datetime.now()
        first_note.save()
        #Ensure we have almost the same updated_at
        self.assertAlmostEqual(first_note.updated_at, now, delta=timedelta(seconds=1))
