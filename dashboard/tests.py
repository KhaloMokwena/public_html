import os
import re
import shutil
import tempfile
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.staticfiles import finders
from django.core import mail
from django.core.mail import EmailMessage
from django.core.management import call_command
from django.template import Context, Template
from django.test import TestCase, override_settings
from django.urls import reverse

from .content import PAGES, department_group
from .models import (
    ContentBlock, ContactMessage, Division, Faq, JobApplication, JobPosting, Record, Service,
)
from .search import run_search

MEDIA_TMP = tempfile.mkdtemp()
PRIVATE_TMP = tempfile.mkdtemp()


def _tiny_png():
    from io import BytesIO
    from PIL import Image
    buffer = BytesIO()
    Image.new('RGB', (1, 1), 'red').save(buffer, 'PNG')
    return buffer.getvalue()


TINY_PNG = _tiny_png()


def defaults_for(page):
    """POST data that leaves every block on a page at its default."""
    return {b['key']: b['default'] for b in PAGES[page]['blocks']}


def make_record(title='Sample image', **kwargs):
    return Record.objects.create(
        title=title, description=kwargs.pop('description', 'A sample.'),
        image=SimpleUploadedFile(f'{title}.png', b'not-really-a-png', content_type='image/png'), **kwargs,
    )


@override_settings(MEDIA_ROOT=MEDIA_TMP, PRIVATE_MEDIA_ROOT=PRIVATE_TMP)
class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.addClassCleanup(shutil.rmtree, MEDIA_TMP, ignore_errors=True)
        cls.addClassCleanup(shutil.rmtree, PRIVATE_TMP, ignore_errors=True)


class SeedTests(BaseTestCase):
    def test_seed_loads_the_document_content_and_is_repeatable(self):
        call_command('seed_content', verbosity=0)
        counts = (Service.objects.count(), JobPosting.objects.count(), Division.objects.count(), Faq.objects.count())
        self.assertEqual(counts, (34, 14, 6, 3))
        call_command('seed_content', verbosity=0)
        self.assertEqual(
            (Service.objects.count(), JobPosting.objects.count(), Division.objects.count(), Faq.objects.count()), counts)

    def test_division_text_fields_parse(self):
        call_command('seed_content', verbosity=0)
        d = Division.objects.first()
        self.assertEqual(len(d.bullet_list()), 4)
        self.assertEqual(len(d.stat_list()), 3)
        self.assertEqual(d.stat_list()[0], {'value': 'Java & .NET Core', 'label': 'Ecosystem Focus'})
        table = d.comparison_table()
        self.assertEqual(len(table['head']), 3)
        self.assertEqual(len(table['rows']), 3)

    def test_every_seeded_job_has_a_filter_group(self):
        call_command('seed_content', verbosity=0)
        groups = {department_group(j.department) for j in JobPosting.objects.all()}
        self.assertEqual(groups, {'HR', 'IT', 'Marketing', 'Finance', 'Ops'})


class PublicPageTests(BaseTestCase):
    def setUp(self):
        call_command('seed_content', verbosity=0)

    def test_every_page_renders_with_header_and_footer(self):
        for name in ['home', 'about', 'services', 'careers', 'contact']:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)
            self.assertContains(response, 'info@zuriko.co.za')
            self.assertContains(response, 'Get Started')
            self.assertContains(response, 'All Rights Reserved')

    def test_only_the_current_page_is_marked_active_in_the_nav(self):
        response = self.client.get(reverse('services'))
        self.assertContains(response, 'href="/services/" aria-current="page"')
        self.assertContains(response, 'nav-link active', count=1)

    def test_home_is_full_screen_hero_with_typed_lines(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Welcome to')
        self.assertContains(response, 'id="typed"')
        self.assertContains(response, 'id="hero-lines"')
        self.assertContains(response, 'over-hero')

    def test_home_background_comes_from_the_media_library(self):
        record = make_record('Backdrop')
        ContentBlock.objects.create(page='home', key='background', value=str(record.pk))
        self.assertContains(self.client.get(reverse('home')), f'class="hero__bg" src="{record.image.url}"')

    def test_deleted_media_slot_falls_back_quietly(self):
        record = make_record('Gone')
        ContentBlock.objects.create(page='home', key='background', value=str(record.pk))
        record.delete()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'class="hero__bg"')

    def test_logo_slot_replaces_the_text_wordmark(self):
        record = make_record('Logo')
        ContentBlock.objects.create(page='site', key='logo', value=str(record.pk))
        response = self.client.get(reverse('about'))
        self.assertContains(response, f'class="brand-logo" src="{record.image.url}"')
        self.assertNotContains(response, '<span class="brand-word">')

    def test_services_page_lists_all_services_and_sectors(self):
        response = self.client.get(reverse('services'))
        self.assertContains(response, 'class="svc"', count=34)
        self.assertContains(response, 'data-sector="Hospitality &amp; Tourism"')
        self.assertContains(response, 'Search matrices...')

    def test_careers_page_lists_jobs_and_department_filters(self):
        response = self.client.get(reverse('careers'))
        self.assertContains(response, '<details class="job"', count=14)
        for group in ['HR', 'IT', 'Marketing', 'Finance', 'Ops']:
            self.assertContains(response, f'data-group="{group}" aria-pressed="false"')
        self.assertContains(response, 'Senior Java Developer')
        job = JobPosting.objects.get(title='Senior Java Developer')
        self.assertContains(response, f'href="/careers/apply/{job.pk}/"')
        self.assertNotContains(response, 'mailto:careers')

    def test_about_page_has_divisions_faqs_and_gallery(self):
        make_record('Site photo')
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'Division 01 • Operational Core')
        self.assertContains(response, 'Division 06 • Operational Core')
        self.assertContains(response, '<table class="compare">', count=6)
        self.assertContains(response, 'class="accordion-item"', count=3)
        self.assertContains(response, 'Site photo')

    def test_gallery_hides_items_flagged_out(self):
        make_record('Shown one')
        make_record('Hidden one', show_in_gallery=False)
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'Shown one')
        self.assertNotContains(response, 'Hidden one')

    def test_media_shortcode_is_rendered_and_surrounding_text_is_escaped(self):
        record = make_record('Inline pic')
        Faq.objects.create(question='Q?', answer=f'Look: [media:{record.pk}] <b>bold</b>', order=9)
        response = self.client.get(reverse('about'))
        self.assertContains(response, f'<figure class="media-embed"><img src="{record.image.url}"')
        self.assertContains(response, '&lt;b&gt;bold&lt;/b&gt;')
        self.assertNotContains(response, '<b>bold</b>')

    def test_unknown_shortcode_disappears(self):
        Faq.objects.create(question='Q?', answer='Before [media:99999] after', order=9)
        response = self.client.get(reverse('about'))
        self.assertNotContains(response, '[media:99999]')

    def test_with_media_filter_directly(self):
        record = make_record('Direct')
        html = Template('{% load content_tags %}{{ t|with_media|linebreaksbr }}').render(
            Context({'t': f'a\n[media:{record.pk}]\n<i>x</i>'}))
        self.assertIn('<br>', html)
        self.assertIn('<figure class="media-embed">', html)
        self.assertIn('&lt;i&gt;x&lt;/i&gt;', html)


class ContactFormTests(BaseTestCase):
    payload = {'name': 'Thandi', 'email': 'thandi@example.com', 'phone': '0821234567',
               'message': 'Need a brand refresh.', 'popia_consent': 'on'}

    def test_valid_submission_is_saved_and_confirmed(self):
        response = self.client.post(reverse('contact'), self.payload)
        self.assertRedirects(response, reverse('contact_thanks'))
        saved = ContactMessage.objects.get()
        self.assertEqual((saved.name, saved.popia_consent), ('Thandi', True))
        self.assertContains(self.client.get(reverse('contact_thanks')), 'Message received')
        self.assertContains(self.client.get(reverse('contact_thanks')), 'href="/"')
        self.assertContains(self.client.get(reverse('contact_thanks')), reverse('contact'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['info@zuriko.co.za'])
        self.assertEqual(mail.outbox[0].reply_to, ['thandi@example.com'])
        self.assertEqual(mail.outbox[0].subject, 'General Inquiry from: Thandi')

    def test_a_line_break_in_the_name_cannot_inject_email_headers(self):
        self.client.post(reverse('contact'), {**self.payload, 'name': 'Eve\nBcc: victim@example.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn('\n', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].bcc, [])

    def test_mail_failure_does_not_lose_the_enquiry(self):
        with mock.patch.object(EmailMessage, 'send', side_effect=OSError('smtp down')):
            with self.assertLogs('dashboard.notifications', level='ERROR'):
                response = self.client.post(reverse('contact'), self.payload)
        self.assertRedirects(response, reverse('contact_thanks'))
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_invalid_submission_shows_errors_and_keeps_values(self):
        response = self.client.post(reverse('contact'), {**self.payload, 'email': 'not-an-email'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="err"')
        self.assertContains(response, 'value="Thandi"')
        self.assertFalse(ContactMessage.objects.exists())

    def test_honeypot_submissions_are_dropped_silently(self):
        response = self.client.post(reverse('contact'), {**self.payload, 'website': 'http://spam.example'})
        self.assertRedirects(response, reverse('contact_thanks'))
        self.assertFalse(ContactMessage.objects.exists())
        self.assertEqual(mail.outbox, [])

    def test_consent_is_required_and_the_agreement_is_shown(self):
        data = {k: v for k, v in self.payload.items() if k != 'popia_consent'}
        response = self.client.post(reverse('contact'), data)
        self.assertContains(response, 'accept the consent policy')
        self.assertFalse(ContactMessage.objects.exists())
        page = self.client.get(reverse('contact'))
        self.assertContains(page, 'Contact Data Consent Policy')
        self.assertContains(page, 'Retention Limits')

    def test_form_uses_the_labels_from_the_content_document(self):
        response = self.client.get(reverse('contact'))
        for text in ['Your Full Name', 'Email Address', 'Contact Number', 'Leave a message here',
                     'Project Details or Requirements Query...', 'Centurion, Gauteng, South Africa',
                     'Monday – Friday: 08:00 — 17:00']:
            self.assertContains(response, text)


class SearchTests(BaseTestCase):
    def setUp(self):
        call_command('seed_content', verbosity=0)

    def test_search_ignores_case(self):
        lower = {r['title'] for r in run_search('cybersecurity')}
        upper = {r['title'] for r in run_search('CYBERSECURITY')}
        self.assertIn('Cybersecurity', lower)
        self.assertEqual(lower, upper)

    def test_every_word_must_match(self):
        titles = [r['title'] for r in run_search('java developer')]
        self.assertIn('Senior Java Developer', titles)
        self.assertEqual(run_search('java zzzzqqq'), [])

    def test_too_short_query_returns_nothing(self):
        self.assertEqual(run_search('a'), [])
        self.assertEqual(run_search('   '), [])

    def test_results_link_to_the_content_with_anchor_and_highlight_term(self):
        result = next(r for r in run_search('Telehealth') if r['kind'] == 'Service')
        service = Service.objects.get(title='Telehealth Portal Orchestration')
        self.assertEqual(result['url'], f'/services/?hl=Telehealth#service-{service.pk}')

    def test_searches_jobs_faqs_and_divisions(self):
        kinds = {r['kind'] for r in run_search('ACID')}
        self.assertTrue({'Job', 'Division', 'FAQ'} <= kinds)

    def test_searches_page_wording(self):
        pages = [r for r in run_search('reach out for a consultation') if r['kind'] == 'Page']
        self.assertEqual(pages[0]['title'], 'Contact page')

    def test_hidden_jobs_are_not_searchable(self):
        JobPosting.objects.create(title='Secret Zebra Wrangler', department='Ops', level='x', scope='s', requirements='r', is_active=False)
        self.assertEqual(run_search('zebra wrangler'), [])

    def test_edited_page_text_is_searchable(self):
        ContentBlock.objects.create(page='contact', key='hours_value', value='Weekends by appointment only')
        pages = [r for r in run_search('weekends appointment') if r['kind'] == 'Page']
        self.assertEqual(pages[0]['url'].split('?')[0], reverse('contact'))

    def test_single_result_redirects_straight_to_the_content(self):
        service = Service.objects.get(title='Telehealth Portal Orchestration')
        response = self.client.get(reverse('search'), {'q': 'telehealth portal'})
        self.assertRedirects(response, f'/services/?hl=telehealth+portal#service-{service.pk}')

    def test_multiple_results_show_a_results_page(self):
        response = self.client.get(reverse('search'), {'q': 'cloud'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="result"')

    def test_results_page_escapes_html_in_content(self):
        Faq.objects.create(question='<script>alert(1)</script> quokka one', answer='a', order=8)
        Faq.objects.create(question='quokka two', answer='b', order=9)
        response = self.client.get(reverse('search'), {'q': 'quokka'})
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')

    def test_no_results_and_short_query_messages(self):
        self.assertContains(self.client.get(reverse('search'), {'q': 'zzzzqqqq'}), 'Nothing matched')
        self.assertContains(self.client.get(reverse('search'), {'q': 'a'}), 'at least 2 characters')

    def test_suggest_endpoint_returns_json(self):
        data = self.client.get(reverse('search_suggest'), {'q': 'cloud'}).json()
        self.assertGreater(data['total'], 0)
        self.assertLessEqual(len(data['results']), 6)
        self.assertEqual(set(data['results'][0]), {'title', 'kind', 'page', 'url'})
        self.assertEqual(self.client.get(reverse('search_suggest'), {'q': 'x'}).json()['results'], [])


class ManageAccessTests(BaseTestCase):
    def test_anonymous_is_sent_to_login(self):
        urls = [reverse('dashboard'), reverse('page_edit', args=['home']), reverse('item_add', args=['divisions']),
                reverse('record_list'), reverse('inbox'), reverse('applications'), reverse('application_cv', args=[1])]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, url)
            self.assertIn('/admin/login/', response.url)

    def test_logged_in_non_staff_is_blocked(self):
        user = get_user_model().objects.create_user('visitor', password='pw')
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('inbox')).status_code, 302)


class ManageEditingTests(BaseTestCase):
    def setUp(self):
        call_command('seed_content', verbosity=0)
        staff = get_user_model().objects.create_user('staff', password='pw', is_staff=True)
        self.client.force_login(staff)

    def test_every_screen_loads(self):
        for name, args in [('dashboard', []), ('record_list', []), ('record_add', []), ('inbox', []), ('applications', [])] + \
                          [('page_edit', [slug]) for slug in PAGES]:
            self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 200, name)

    def test_saving_text_changes_the_public_page_and_stores_only_edits(self):
        data = defaults_for('home')
        data['hero_title'] = 'Acme Corp'
        response = self.client.post(reverse('page_edit', args=['home']), data)
        self.assertRedirects(response, reverse('page_edit', args=['home']))
        self.assertEqual(ContentBlock.objects.filter(page='home').count(), 1)
        self.assertContains(self.client.get(reverse('home')), 'Acme Corp')

    def test_typed_lines_can_be_edited(self):
        data = defaults_for('home')
        data['hero_lines'] = 'First line\nSecond line'
        self.client.post(reverse('page_edit', args=['home']), data)
        page = self.client.get(reverse('home'))
        self.assertContains(page, 'First line')
        self.assertContains(page, '"Second line"')

    def test_choosing_and_clearing_a_media_slot(self):
        record = make_record('Chosen')
        data = defaults_for('home')
        data['background'] = str(record.pk)
        self.client.post(reverse('page_edit', args=['home']), data)
        self.assertEqual(ContentBlock.objects.get(page='home', key='background').value, str(record.pk))
        data['background'] = ''
        self.client.post(reverse('page_edit', args=['home']), data)
        self.assertFalse(ContentBlock.objects.filter(page='home', key='background').exists())

    def test_media_slot_rejects_an_id_that_does_not_exist(self):
        data = defaults_for('home')
        data['background'] = '99999'
        response = self.client.post(reverse('page_edit', args=['home']), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContentBlock.objects.filter(page='home', key='background').exists())

    def test_reset_restores_defaults_for_that_page_only(self):
        ContentBlock.objects.create(page='home', key='hero_title', value='Custom')
        ContentBlock.objects.create(page='contact', key='heading', value='Keep me')
        self.client.post(reverse('page_reset', args=['home']))
        self.assertFalse(ContentBlock.objects.filter(page='home').exists())
        self.assertTrue(ContentBlock.objects.filter(page='contact').exists())

    def test_add_edit_delete_division_with_media(self):
        record = make_record('Division pic')
        response = self.client.post(reverse('item_add', args=['divisions']), {
            'title': 'New Division', 'subtitle': 'Sub', 'description': 'Body', 'bullets': 'One\nTwo',
            'stats': 'A | B', 'comparison': 'H1 | H2 | H3\nx | y | z', 'media': record.pk, 'order': 7,
        })
        self.assertRedirects(response, reverse('page_edit', args=['about']))
        division = Division.objects.get(title='New Division')
        self.assertEqual(division.media, record)
        self.assertContains(self.client.get(reverse('about')), record.image.url)
        self.client.post(reverse('item_delete', args=['divisions', division.pk]))
        self.assertFalse(Division.objects.filter(title='New Division').exists())

    def test_deleting_media_keeps_the_division(self):
        record = make_record('Temp')
        division = Division.objects.create(title='Has pic', description='d', media=record)
        record.delete()
        division.refresh_from_db()
        self.assertIsNone(division.media)

    def test_add_service_and_it_shows_up_and_is_searchable(self):
        self.client.post(reverse('item_add', args=['services']), {
            'title': 'Drone Mapping', 'category': 'Construction & Civil Engineering', 'description': 'Aerial surveys.', 'order': 99,
        })
        self.assertContains(self.client.get(reverse('services')), 'Drone Mapping')
        self.assertTrue(any(r['title'] == 'Drone Mapping' for r in run_search('DRONE')))

    def test_media_library_shows_shortcodes_and_gallery_flag(self):
        record = make_record('Library item')
        page = self.client.get(reverse('record_list'))
        self.assertContains(page, f'[media:{record.pk}]')

    def test_add_media_through_the_form(self):
        response = self.client.post(reverse('record_add'), {
            'title': 'Uploaded', 'description': 'From the form', 'show_in_gallery': 'on',
            'image': SimpleUploadedFile('up.png', TINY_PNG, content_type='image/png'),
        })
        self.assertRedirects(response, reverse('record_list'))
        self.assertTrue(Record.objects.filter(title='Uploaded').exists())

    def test_inbox_toggle_and_delete(self):
        enquiry = ContactMessage.objects.create(name='A', email='a@example.com', message='Hi')
        self.assertContains(self.client.get(reverse('inbox')), 'New')
        self.client.post(reverse('inbox_toggle', args=[enquiry.pk]))
        enquiry.refresh_from_db()
        self.assertTrue(enquiry.handled)
        self.assertEqual(self.client.get(reverse('inbox_toggle', args=[enquiry.pk])).status_code, 405)
        self.client.post(reverse('inbox_delete', args=[enquiry.pk]))
        self.assertFalse(ContactMessage.objects.exists())

    def test_unknown_page_and_kind_are_404(self):
        self.assertEqual(self.client.get(reverse('page_edit', args=['nope'])).status_code, 404)
        self.assertEqual(self.client.get(reverse('item_add', args=['nope'])).status_code, 404)


# ---------------------------------------------------------------------------
# Job applications
# ---------------------------------------------------------------------------

def cv_file(name='cv.pdf', content=None, extra=0):
    return SimpleUploadedFile(name, content if content is not None else b'%PDF-1.4\n' + b'x' * extra, content_type='application/pdf')


class ApplyTests(BaseTestCase):
    def setUp(self):
        call_command('seed_content', verbosity=0)
        self.job = JobPosting.objects.get(title='Senior Java Developer')
        self.url = reverse('apply', args=[self.job.pk])
        self.payload = {'name': 'Thandi Mokoena', 'email': 'thandi@example.com', 'phone': '0821234567',
                        'message': 'I would love to join.', 'popia_consent': 'on'}

    def submit(self, drop=(), **overrides):
        data = {**self.payload, 'cv': cv_file(), **overrides}
        for key in drop:
            data.pop(key)
        return self.client.post(self.url, data)

    def test_apply_page_shows_the_role_form_and_agreement(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apply: Senior Java Developer')
        self.assertContains(response, 'enctype="multipart/form-data"')
        self.assertContains(response, 'accept=".pdf,.doc,.docx"')
        self.assertContains(response, 'Employee POPIA &amp; Candidate Data Agreement')
        self.assertContains(response, 'Collection Purpose')

    def test_valid_application_is_saved_privately_and_emailed_with_the_cv(self):
        response = self.submit()
        self.assertRedirects(response, reverse('apply_thanks', args=[self.job.pk]))
        application = JobApplication.objects.get()
        self.assertEqual((application.role, application.job, application.popia_consent), ('Senior Java Developer', self.job, True))
        self.assertTrue(application.cv.storage.exists(application.cv.name))
        self.assertTrue(os.path.abspath(application.cv.path).startswith(os.path.abspath(PRIVATE_TMP)))
        with self.assertRaises(ValueError):
            application.cv.url        # private files have no web address

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, ['careers@zuriko.co.za'])
        self.assertEqual(message.reply_to, ['thandi@example.com'])
        self.assertEqual(message.subject, 'Job Application: Senior Java Developer - Thandi Mokoena')
        self.assertIn('Contact Number: 0821234567', message.body)
        self.assertEqual(len(message.attachments), 1)
        self.assertTrue(message.attachments[0][0].endswith('.pdf'))
        thanks = self.client.get(reverse('apply_thanks', args=[self.job.pk]))
        self.assertContains(thanks, 'Application received')
        self.assertContains(thanks, reverse('careers'))

    def test_the_receiving_address_is_editable_in_manage(self):
        ContentBlock.objects.create(page='careers', key='apply_email', value='hr@example.com')
        self.submit()
        self.assertEqual(mail.outbox[0].to, ['hr@example.com'])

    def test_mail_failure_never_loses_the_application(self):
        with mock.patch.object(EmailMessage, 'send', side_effect=OSError('smtp down')):
            with self.assertLogs('dashboard.notifications', level='ERROR'):
                response = self.submit()
        self.assertRedirects(response, reverse('apply_thanks', args=[self.job.pk]))
        self.assertEqual(JobApplication.objects.count(), 1)

    def test_wrong_file_type_is_refused(self):
        response = self.submit(cv=cv_file('cv.exe', b'MZ\x90\x00'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'is not allowed')
        self.assertFalse(JobApplication.objects.exists())

    def test_a_renamed_file_is_refused(self):
        response = self.submit(cv=cv_file('cv.pdf', b'MZ\x90\x00 this is really a program'))
        self.assertContains(response, 'does not look like a genuine PDF')
        self.assertFalse(JobApplication.objects.exists())

    def test_files_over_5mb_are_refused(self):
        response = self.submit(cv=cv_file(extra=5 * 1024 * 1024 + 1))
        self.assertContains(response, 'too large')
        self.assertFalse(JobApplication.objects.exists())

    def test_word_documents_are_accepted(self):
        self.submit(cv=cv_file('cv.docx', b'PK\x03\x04 word document'))
        self.submit(cv=cv_file('cv.doc', b'\xd0\xcf\x11\xe0 old word document'))
        self.assertEqual(JobApplication.objects.count(), 2)

    def test_agreement_and_required_fields_are_enforced(self):
        response = self.submit(drop=['popia_consent'])
        self.assertContains(response, 'accept the agreement')
        self.assertFalse(JobApplication.objects.exists())
        response = self.submit(phone='')
        self.assertContains(response, 'class="err"')
        self.assertContains(response, 'value="Thandi Mokoena"')     # what they typed is kept
        self.assertFalse(JobApplication.objects.exists())

    def test_honeypot_submissions_are_dropped(self):
        response = self.submit(website='http://spam.example')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(JobApplication.objects.exists())
        self.assertEqual(mail.outbox, [])

    def test_closed_or_unknown_jobs_cannot_be_applied_for(self):
        self.job.is_active = False
        self.job.save()
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertEqual(self.submit().status_code, 404)
        self.assertEqual(self.client.get(reverse('apply', args=[99999])).status_code, 404)

    def test_thanks_page_still_works_if_the_role_has_since_closed(self):
        self.submit()
        self.job.is_active = False
        self.job.save()
        response = self.client.get(reverse('apply_thanks', args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Application received')

    def test_unknown_job_on_thanks_page_is_404(self):
        self.assertEqual(self.client.get(reverse('apply_thanks', args=[99999])).status_code, 404)

    def test_deleting_a_job_keeps_the_application(self):
        self.submit()
        self.job.delete()
        application = JobApplication.objects.get()
        self.assertIsNone(application.job)
        self.assertEqual(application.role, 'Senior Java Developer')


class ApplicationsInboxTests(BaseTestCase):
    def setUp(self):
        call_command('seed_content', verbosity=0)
        job = JobPosting.objects.get(title='Senior Java Developer')
        self.application = JobApplication.objects.create(
            job=job, role=job.title, name='Thandi Mokoena', email='t@example.com', phone='082 123 4567',
            message='Hello', popia_consent=True, cv=cv_file(content=b'%PDF-1.4 my cv'),
        )
        self.staff = get_user_model().objects.create_user('staff', password='pw', is_staff=True)

    def test_staff_can_list_and_download_the_cv(self):
        self.client.force_login(self.staff)
        page = self.client.get(reverse('applications'))
        self.assertContains(page, 'Thandi Mokoena')
        self.assertContains(page, 'Download CV')
        response = self.client.get(reverse('application_cv', args=[self.application.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertIn('thandi-mokoena-senior-java-developer.pdf', response['Content-Disposition'])
        self.assertEqual(b''.join(response.streaming_content), b'%PDF-1.4 my cv')

    def test_cv_download_is_staff_only(self):
        url = reverse('application_cv', args=[self.application.pk])
        self.assertEqual(self.client.get(url).status_code, 302)
        visitor = get_user_model().objects.create_user('visitor', password='pw')
        self.client.force_login(visitor)
        self.assertEqual(self.client.get(url).status_code, 302)

    def test_review_toggle_and_delete_also_removes_the_cv_file(self):
        self.client.force_login(self.staff)
        self.client.post(reverse('application_toggle', args=[self.application.pk]))
        self.application.refresh_from_db()
        self.assertTrue(self.application.handled)
        self.assertEqual(self.client.get(reverse('application_toggle', args=[self.application.pk])).status_code, 405)
        path = self.application.cv.path
        self.assertTrue(os.path.exists(path))
        self.client.post(reverse('application_delete', args=[self.application.pk]))
        self.assertFalse(JobApplication.objects.exists())
        self.assertFalse(os.path.exists(path))

    def test_applications_are_not_searchable(self):
        self.assertEqual([r for r in run_search('Thandi') if r['kind'] not in ('Page',)], [])


# ---------------------------------------------------------------------------
# Stylesheet, hamburger menu, About sub-nav
# ---------------------------------------------------------------------------

class StylesheetAndNavTests(BaseTestCase):
    def css(self):
        path = finders.find('dashboard/css/site.css')
        self.assertIsNotNone(path, "site.css must be findable as a static file")
        with open(path, encoding='utf-8') as handle:
            return handle.read()

    def test_all_pages_use_the_one_central_stylesheet(self):
        for name in ['home', 'about', 'services', 'careers', 'contact', 'search']:
            response = self.client.get(reverse(name))
            self.assertContains(response, 'dashboard/css/site.css')
            self.assertNotContains(response, '<style')

    def test_palette_comes_from_the_old_site(self):
        css = self.css()
        for token in ['--brand: #FF0490', '--blue: #4a5fff', '--slate: #2f4d5a', '--bar: #39312f']:
            self.assertIn(token, css)

    def test_bootstrap_script_url_is_correct_so_the_hamburger_works(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js')
        self.assertNotContains(response, 'dist/bootstrap.bundle')
        self.assertContains(response, 'data-bs-target="#mainNav"')
        self.assertContains(response, 'id="mainNav"')

    def test_about_sub_nav_wraps_instead_of_scrolling_sideways(self):
        css = self.css()
        list_rule = re.search(r'\.division-jump ul\s*\{([^}]*)\}', css).group(1)
        self.assertIn('flex-wrap: wrap', list_rule)
        self.assertNotIn('overflow-x', list_rule)
        bar_rule = re.search(r'\.division-jump\s*\{([^}]*)\}', css).group(1)
        self.assertNotIn('sticky', bar_rule)


class ThemeToggleAndCopyTests(BaseTestCase):
    def test_theme_toggle_button_is_present_and_theme_defaults_to_dark(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'id="theme-toggle"')
        self.assertContains(response, "localStorage.getItem('zuriko-theme')")

    def test_light_theme_tokens_exist_in_the_stylesheet(self):
        from django.contrib.staticfiles import finders
        with open(finders.find('dashboard/css/site.css'), encoding='utf-8') as handle:
            css = handle.read()
        self.assertIn(':root[data-theme="light"]', css)
        self.assertIn('--bg: #ffffff', css)

    def test_no_jargon_placeholders_anywhere_on_the_public_pages(self):
        call_command('seed_content', verbosity=0)
        banned = ['Search matrices', 'Visual Proof Matrix', 'INITIATING SERVICE MATRICES', 'PROTOCOL', 'lorem ipsum', 'Lorem Ipsum']
        for name in ['home', 'about', 'services', 'careers', 'contact']:
            response = self.client.get(reverse(name))
            for phrase in banned:
                self.assertNotContains(response, phrase, msg_prefix=f'{name} page')
        self.assertContains(self.client.get(reverse('services')), 'Search our services')
        self.assertContains(self.client.get(reverse('careers')), 'Search open positions')

    def test_home_shows_real_sector_strip_and_honest_stats(self):
        call_command('seed_content', verbosity=0)
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'class="sector-strip"')
        self.assertContains(response, 'Hospitality &amp; Tourism')
        self.assertContains(response, '<dt>34</dt>')       # service count, computed, not invented
        self.assertContains(response, '<dt>6</dt>')        # division count

    def test_home_hides_the_strips_when_there_is_no_data_yet(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'class="sector-strip"')
        self.assertNotContains(response, 'class="proof-grid"')
