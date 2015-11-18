from django.test import TestCase
from .models import Participant
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from model_mommy import mommy
from .forms import ParticipantForm


class ParticipantTestCase(TestCase):

    def setUp(self):
        """Se crean participantes de prueba"""
        Participant.objects.create(first_name="Roberto", last_name="Covarrubias", age="24", gender="Male")
        Participant.objects.create(first_name="Luis Salvador", last_name="Lopez Hernandez", age="27", gender="Male")
        Participant.objects.create(first_name="Maria Oyuki", last_name="Fuentes Uc", age="24", gender="Female")


    def test_participant_created(self):
        """Se prueba que los participantes creados en el setup existan"""
        participant1 = Participant.objects.get(first_name="Roberto")
        participant2 = Participant.objects.get(last_name="Lopez Hernandez")
        participant3 = Participant.objects.get(first_name="Maria Oyuki", age="24")
        self.assertEqual(participant1.last_name, 'Covarrubias')
        self.assertEqual(participant2.first_name, 'Luis Salvador')
        self.assertEqual(participant3.last_name, 'Fuentes Uc')


    def test_participant_updated(self):
        """Se prueba que los participantes creados en el setup se puedan actualizar"""
        participant1 = Participant.objects.get(first_name="Roberto")
        participant1.last_name="Covarrubias Carrillo"
        participant1.save()
        participant1_updated = Participant.objects.get(first_name="Roberto")
        self.assertEqual(participant1_updated.last_name, 'Covarrubias Carrillo')


    def test_participant_deleted(self):
        """Se prueba que los participantes creados en el setup se puedan eliminar"""
        participant1 = Participant.objects.get(first_name="Roberto")
        id = participant1.id
        participant1.delete()
        self.assertEqual(False, (Participant.objects.filter(id=id).exists()))



#PRUEBAS AUTO GENERADAS DEL CRUD

class ParticipantTest(WebTest):
    def test_factory_create(self):
        """
        Test that we can create an instance via our object factory.
        """
        instance = mommy.make(Participant)
        self.assertTrue(isinstance(instance, Participant))

    def test_list_view(self):
        """
        Test that the list view returns at least our factory created instance.
        """
        instance = mommy.make(Participant)
        response = self.app.get(reverse('participants:list'))
        object_list = response.context['object_list']
        self.assertIn(instance, object_list)

    # def test_create_view(self):
    #     """
    #     Test that we can create an instance via the create view.
    #     """
    #     response = self.app.get(reverse('participants:create'))
    #     new_name = 'Participant x'
    #
    #     # check that we don't already have a model with this name
    #     self.assertFalse(Participant.objects.filter(first_name=new_name).exists())
    #
    #     form = response.forms[ParticipantForm]
    #     form['first_name'] = new_name
    #     form['last_name'] = new_name
    #     form['age'] = "20"
    #     form['gender'] = "Female"
    #     form.submit().follow()
    #
    #     instance = Participant.objects.get(first_name=new_name)
    #     self.assertEqual(instance.first_name, new_name)

    def test_detail_view(self):
        """
        Test that we can view an instance via the detail view.
        """
        instance = mommy.make(Participant)
        response = self.app.get(instance.get_absolute_url())
        self.assertEqual(response.context['object'], instance)

    def test_update_view(self):
        """
        Test that we can update an instance via the update view.
        """
        instance = mommy.make(Participant)
        response = self.app.get(reverse('participants:update', kwargs={'pk': instance.pk, }))

        form = response.forms['participant_form']
        new_name = 'Some new thing'
        form['name'] = new_name
        form.submit().follow()

        instance = Participant.objects.get(pk=instance.pk)
        self.assertEqual(instance.name, new_name)

    # def test_delete_view(self):
    #     """
    #     Test that we can delete an instance via the delete view.
    #     """
    #     instance = mommy.make(Participant)
    #     pk = instance.pk
    #     response = self.app.get(reverse('participants:delete', kwargs={'pk': pk, }))
    #     response = response.form.submit().follow()
    #     self.assertFalse(Participant.objects.filter(pk=pk).exists())
