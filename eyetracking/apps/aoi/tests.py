from django.core.urlresolvers import reverse
from django_webtest import WebTest
from model_mommy import mommy
from .models import AOI


class AOITest(WebTest):
    def test_factory_create(self):
        """
        Test that we can create an instance via our object factory.
        """
        instance = mommy.make(AOI)
        self.assertTrue(isinstance(instance, AOI))

    def test_list_view(self):
        """
        Test that the list view returns at least our factory created instance.
        """
        instance = mommy.make(AOI)
        response = self.app.get(reverse('aoi:list'))
        object_list = response.context['object_list']
        self.assertIn(instance, object_list)

    def test_create_view(self):
        """
        Test that we can create an instance via the create view.
        """
        response = self.app.get(reverse('aoi:create'))
        new_name = 'A freshly created thing'

        # check that we don't already have a model with this name
        self.assertFalse(AOI.objects.filter(name=new_name).exists())

        form = response.forms['aoi_form']
        form['name'] = new_name
        form.submit().follow()

        instance = AOI.objects.get(name=new_name)
        self.assertEqual(instance.name, new_name)

    def test_detail_view(self):
        """
        Test that we can view an instance via the detail view.
        """
        instance = mommy.make(AOI)
        response = self.app.get(instance.get_absolute_url())
        self.assertEqual(response.context['object'], instance)

    def test_update_view(self):
        """
        Test that we can update an instance via the update view.
        """
        instance = mommy.make(AOI)
        response = self.app.get(reverse('aoi:update', kwargs={'pk': instance.pk, }))

        form = response.forms['aoi_form']
        new_name = 'Some new thing'
        form['name'] = new_name
        form.submit().follow()

        instance = AOI.objects.get(pk=instance.pk)
        self.assertEqual(instance.name, new_name)

    def test_delete_view(self):
        """
        Test that we can delete an instance via the delete view.
        """
        instance = mommy.make(AOI)
        pk = instance.pk
        response = self.app.get(reverse('aoi:delete', kwargs={'pk': pk, }))
        response = response.form.submit().follow()
        self.assertFalse(AOI.objects.filter(pk=pk).exists())
