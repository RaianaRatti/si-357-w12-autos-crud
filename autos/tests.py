from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from autos.models import Auto, Make


# Walks through the same steps the autograder takes
class AutosCrudTest(TestCase):
    def setUp(self):
        User.objects.create_user('dj4e_user', password='Meow_5dfff5_42')

    def test_login_required(self):
        response = self.client.get(reverse('autos:all'))
        self.assertRedirects(response, '/accounts/login/?next=/autos/')

    def test_crud_flow(self):
        c = self.client
        all_url = reverse('autos:all')

        # Log in
        response = c.post(reverse('login'),
                          {'username': 'dj4e_user', 'password': 'Meow_5dfff5_42', 'next': '/autos/'})
        self.assertRedirects(response, all_url)

        # Add a make
        response = c.post(reverse('autos:make_create'), {'name': 'Ford'})
        self.assertRedirects(response, all_url)
        ford = Make.objects.get(name='Ford')

        # Add an auto selecting the make
        response = c.post(reverse('autos:auto_create'),
                          {'nickname': 'Blue', 'mileage': 1000, 'comments': 'Nice', 'make': ford.id})
        self.assertRedirects(response, all_url)
        blue = Auto.objects.get(nickname='Blue')

        # View the makes
        self.assertContains(c.get(reverse('autos:make_list')), 'Ford')

        # Update the make form has a Cancel button that goes to the auto list
        response = c.get(reverse('autos:make_update', args=[ford.id]))
        self.assertContains(response, "window.location='/autos/'")

        # Update the make and save - the auto list shows the new make
        response = c.post(reverse('autos:make_update', args=[ford.id]), {'name': 'Fjord'})
        self.assertRedirects(response, all_url)
        self.assertContains(c.get(all_url), 'Blue (Fjord)')

        # Update the auto nickname
        response = c.post(reverse('autos:auto_update', args=[blue.id]),
                          {'nickname': 'Azure', 'mileage': 1000, 'comments': 'Nice', 'make': ford.id})
        self.assertRedirects(response, all_url)
        self.assertContains(c.get(all_url), 'Azure (Fjord)')

        # Add a second make and a second auto using it
        c.post(reverse('autos:make_create'), {'name': 'Tata'})
        tata = Make.objects.get(name='Tata')
        c.post(reverse('autos:auto_create'),
               {'nickname': 'Red', 'mileage': 5, 'comments': 'Fast', 'make': tata.id})
        self.assertContains(c.get(all_url), 'Red (Tata)')

        # Delete the second make - its auto goes away too (cascade)
        self.assertContains(c.get(reverse('autos:make_delete', args=[tata.id])), 'Tata')
        response = c.post(reverse('autos:make_delete', args=[tata.id]))
        self.assertRedirects(response, all_url)
        self.assertNotContains(c.get(all_url), 'Red')
        self.assertFalse(Auto.objects.filter(nickname='Red').exists())

        # Delete the first auto
        response = c.post(reverse('autos:auto_delete', args=[blue.id]))
        self.assertRedirects(response, all_url)
        self.assertEqual(Auto.objects.count(), 0)

    def test_page_has_dj4e_meta(self):
        self.client.login(username='dj4e_user', password='Meow_5dfff5_42')
        response = self.client.get(reverse('autos:all'))
        self.assertContains(response, '<meta name="dj4e" content="05dfff5cf7a5d8bde1ee6e8951cc382b">')
        self.assertContains(response, '<meta name="dj4e-code" content="42179331938730">')
        self.assertNotContains(response, '42-42')
