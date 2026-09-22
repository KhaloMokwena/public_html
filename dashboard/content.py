"""
Registry of the editable text and media slots on each public page.

Each block has:
  key        - identifier used in templates:  {% page_text 'home' 'hero_title' %}
  label      - what the editor sees in /manage/
  default    - the wording used until someone overrides it
  multiline  - optional, shows a larger text box
  help       - optional, small hint under the field
  type       - optional. 'media' makes it a picker over the media library (Records);
               the chosen image is used with {% page_media 'page' 'key' %}

Overrides are stored in the ContentBlock table (media slots store the Record id).
A block with no override falls back to the default here, so the public site always renders.
"""

BANNER_SLOT = {
    'key': 'banner', 'type': 'media', 'default': '',
    'label': 'Banner image behind the page heading (optional)',
}

PAGES = {
    'site': {
        'label': 'Site-wide',
        'url_name': 'home',
        'blocks': [
            {'key': 'email', 'label': 'Email (top bar and footer)', 'default': 'info@zuriko.co.za'},
            {'key': 'phone', 'label': 'Phone (top bar)', 'default': '+2760 287 2446'},
            {'key': 'cta_label', 'label': 'Top bar button (goes to Contact)', 'default': 'Get Started'},
            {'key': 'logo', 'type': 'media', 'default': '', 'label': 'Logo image',
             'help': 'Pick an image from the Media library. Without one, the name below is shown as text.'},
            {'key': 'brand_name', 'label': 'Name shown when there is no logo image', 'default': 'ZuriKO'},
            {'key': 'logo_alt', 'label': 'Logo description (for screen readers)', 'default': 'Zuriko company logo'},
            {'key': 'nav_home', 'label': 'Menu: Home', 'default': 'Home'},
            {'key': 'nav_about', 'label': 'Menu: About', 'default': 'About'},
            {'key': 'nav_services', 'label': 'Menu: Services', 'default': 'Services'},
            {'key': 'nav_careers', 'label': 'Menu: Careers', 'default': 'Careers'},
            {'key': 'nav_contact', 'label': 'Menu: Contact', 'default': 'Contact'},
            {'key': 'search_placeholder', 'label': 'Search box hint', 'default': 'Search the site...'},
            {'key': 'copyright', 'label': 'Footer: copyright line', 'default': '© Copyright ZuriKO Technologies. All Rights Reserved'},
            {'key': 'credit', 'label': 'Footer: credit line', 'default': 'Designed by ZuriKO Technologies'},
        ],
        'collections': [],
    },
    'home': {
        'label': 'Home',
        'url_name': 'home',
        'blocks': [
            {'key': 'background', 'type': 'media', 'default': '',
             'label': 'Full-screen background image',
             'help': 'Pick an image from the Media library. Without one, a dark gradient is shown.'},
            {'key': 'welcome_label', 'label': 'Title, first line', 'default': 'Welcome to'},
            {'key': 'hero_title', 'label': 'Title, second line', 'default': 'ZuriKO Technologies'},
            {'key': 'hero_lines', 'label': 'Typed subtitle (one phrase per line)', 'multiline': True,
             'default': ('Your IT & Media Partner for Innovation\n'
                         'Enterprise Software Engineering & Architecture\n'
                         'Broadcast Media, HD Videography & Sound Engineering\n'
                         'Elite Brand Strategy & Visual Identity Design'),
             'help': 'Each line is typed out, held, deleted, then the next one starts. Keep a single line and it types once and stays.'},
            {'key': 'strip_label', 'label': 'Small label above the sector strip', 'default': 'Industries we work with'},
            {'key': 'proof_label', 'label': 'Small label above the numbers row', 'default': 'At a glance'},
        ],
        'collections': [],
    },
    'about': {
        'label': 'About',
        'url_name': 'about',
        'blocks': [
            BANNER_SLOT,
            {'key': 'kicker', 'label': 'Small label above the heading', 'default': 'Corporate Capabilities Profile'},
            {'key': 'heading', 'label': 'Page heading', 'default': 'ZuriKO Technologies: Engineering Modern Digital Ecosystems'},
            {'key': 'intro', 'label': 'Intro paragraph', 'multiline': True,
             'default': ('ZuriKO Technologies operates as a premier multi-disciplinary enterprise modernization and brand '
                         'transformation collective based in Centurion, South Africa. We engineering fault-tolerant backend '
                         'infrastructures, high-conversion user interfaces, and corporate media structures designed to perform '
                         'under intensive real-world workflows. Moving away from standard consulting models, we treat software '
                         'engineering and visual identity as a single unified layer. Our backend architectures prioritize rigid '
                         'multi-threaded stability, data compliance, and transactional safety, while our creative studio builds '
                         'unforgettable, highly cohesive brand identities that command instant market authority.'),
             'help': 'Type [media:ID] to place a Media library image inside the text.'},
            {'key': 'division_tag', 'label': 'Text after "Division 01 •"', 'default': 'Operational Core'},
            {'key': 'faq_label', 'label': 'FAQ section: small label', 'default': 'Architectural FAQ'},
            {'key': 'faq_heading', 'label': 'FAQ section: heading', 'default': 'Frequently Asked Technical Operations'},
            {'key': 'faq_empty', 'label': 'FAQ section: text when there are no FAQs', 'default': 'No FAQs have been added yet.'},
            {'key': 'gallery_label', 'label': 'Gallery: small label', 'default': 'Our Work'},
            {'key': 'gallery_heading', 'label': 'Gallery: heading', 'default': 'Enterprise Production Infrastructure'},
            {'key': 'gallery_text', 'label': 'Gallery: description', 'multiline': True,
             'default': ('A transparent structural overview highlighting our core production runs, wide-format signs '
                         'deployments, and media staging configurations across Gauteng.')},
            {'key': 'gallery_empty', 'label': 'Gallery: text when there are no images', 'default': 'Images will appear here as they are added to the Media library.'},
        ],
        'collections': ['divisions', 'faqs'],
    },
    'services': {
        'label': 'Services',
        'url_name': 'services',
        'blocks': [
            BANNER_SLOT,
            {'key': 'heading', 'label': 'Page heading', 'default': 'Our Specialized Enterprise Solutions'},
            {'key': 'intro', 'label': 'Intro paragraph', 'multiline': True,
             'default': ('ZuriKO Technologies delivers high-performance technical engineering and production structures across '
                         'multiple business sectors in South Africa. Filter our catalog below or search for specific tools.')},
            {'key': 'search_placeholder', 'label': 'Search box hint', 'default': 'Search our services...'},
            {'key': 'filter_label', 'label': 'Label above the industry filter buttons', 'default': 'Filter by industry'},
            {'key': 'all_label', 'label': 'Filter button for everything', 'default': 'All'},
            {'key': 'no_match_text', 'label': 'Text when the search finds nothing', 'default': 'No services match your search.'},
            {'key': 'empty_text', 'label': 'Text when there are no services at all', 'default': 'No services have been added yet.'},
        ],
        'collections': ['services'],
    },
    'careers': {
        'label': 'Careers',
        'url_name': 'careers',
        'blocks': [
            BANNER_SLOT,
            {'key': 'heading', 'label': 'Page heading', 'default': 'Join the ZuriKO Team'},
            {'key': 'intro', 'label': 'Intro paragraph', 'multiline': True,
             'default': ('We are building a robust, versatile team capable of scaling a dynamic SMME in South Africa. We are always '
                         'looking for passionate innovators to join our divisions. All positions are offered on a hybrid work model '
                         'for candidates based in Centurion or surrounding areas.')},
            {'key': 'search_placeholder', 'label': 'Search box hint', 'default': 'Search open positions...'},
            {'key': 'filter_label', 'label': 'Label above the department filter buttons', 'default': 'Filter by department'},
            {'key': 'all_label', 'label': 'Filter button for everything', 'default': 'All'},
            {'key': 'scope_heading', 'label': 'Heading over each job\'s scope', 'default': 'Scope'},
            {'key': 'requirements_heading', 'label': 'Heading over each job\'s requirements', 'default': 'Requirements'},
            {'key': 'apply_button', 'label': 'Apply button text', 'default': 'Apply for this role'},
            {'key': 'apply_email', 'label': 'Email that receives new applications (with the CV attached)', 'default': 'careers@zuriko.co.za'},
            {'key': 'apply_intro', 'label': 'Apply page: intro text', 'multiline': True,
             'default': 'Send us your details and CV. We only use them to assess your fit for this role.'},
            {'key': 'apply_submit', 'label': 'Apply page: submit button', 'default': 'Submit Application'},
            {'key': 'apply_success_heading', 'label': 'Apply page: confirmation heading', 'default': 'Application received'},
            {'key': 'apply_success_text', 'label': 'Apply page: confirmation text', 'multiline': True,
             'default': 'Thank you for applying. Our HR team will review your application and be in touch.'},
            {'key': 'consent_label', 'label': 'Apply page: text before the agreement link', 'default': 'I agree to the'},
            {'key': 'popia_title', 'label': 'Agreement: title', 'default': 'Employee POPIA & Candidate Data Agreement'},
            {'key': 'popia_text', 'label': 'Agreement: full text', 'multiline': True,
             'default': ('1. Collection Purpose\n'
                         'ZuriKO Technologies collects and processes candidate background variables solely to triage operational fit '
                         'against active recruitment metrics within our IT and Media divisions.\n\n'
                         '2. Data Retention Parameters\n'
                         '- Unsuccessful application files are completely scrubbed inside 6 calendar months.\n'
                         '- Secure storage profiles are restricted solely to internal Human Resource executives.\n'
                         '- Candidates reserve absolute rights to request immediate profiling removal at any point by contacting talent@zuriko.co.za.\n\n'
                         '3. Security Declaration\n'
                         'All submitted data, summaries of experience, and contact endpoints are locked behind industry-standard cloud '
                         'encryption profiles to prevent unauthorized access.'),
             'help': 'Carried over from your old popia_employee.json. Have it reviewed against how applications are actually handled.'},
            {'key': 'no_match_text', 'label': 'Text when the search finds nothing', 'default': 'No positions match your search.'},
            {'key': 'empty_text', 'label': 'Text when there are no open positions', 'default': 'There are no open positions at the moment.'},
        ],
        'collections': ['jobs'],
    },
    'contact': {
        'label': 'Contact',
        'url_name': 'contact',
        'blocks': [
            BANNER_SLOT,
            {'key': 'heading', 'label': 'Page heading', 'default': 'Connect with our Engineering Team'},
            {'key': 'connect_heading', 'label': 'Left column heading', 'default': "Let's Connect"},
            {'key': 'connect_text', 'label': 'Left column text', 'default': 'Ready to transform your brand? Reach out for a consultation.'},
            {'key': 'hub_label', 'label': 'Address: label', 'default': 'Our Operations Hub'},
            {'key': 'hub_value', 'label': 'Address: value', 'default': 'Centurion, Gauteng, South Africa'},
            {'key': 'intake_label', 'label': 'Email: label', 'default': 'General Intake Queries'},
            {'key': 'intake_value', 'label': 'Email: value', 'default': 'info@zuriko.co.za'},
            {'key': 'hours_label', 'label': 'Hours: label', 'default': 'Operational Availability'},
            {'key': 'hours_value', 'label': 'Hours: value', 'default': 'Monday – Friday: 08:00 — 17:00'},
            {'key': 'name_label', 'label': 'Name field: label', 'default': 'Your Full Name'},
            {'key': 'name_placeholder', 'label': 'Name field: example text', 'default': 'John Doe'},
            {'key': 'email_label', 'label': 'Email field: label', 'default': 'Email Address'},
            {'key': 'email_placeholder', 'label': 'Email field: example text', 'default': 'name@example.com'},
            {'key': 'phone_label', 'label': 'Phone field: label', 'default': 'Contact Number'},
            {'key': 'phone_placeholder', 'label': 'Phone field: example text', 'default': '0821234567'},
            {'key': 'message_label', 'label': 'Message field: label', 'default': 'Project Details or Requirements Query...'},
            {'key': 'message_placeholder', 'label': 'Message field: example text', 'default': 'Leave a message here'},
            {'key': 'submit_button', 'label': 'Send button', 'default': 'Send Message'},
            {'key': 'consent_label', 'label': 'Text before the agreement link', 'default': 'I agree to the'},
            {'key': 'popia_title', 'label': 'Agreement: title', 'default': 'Contact Data Consent Policy'},
            {'key': 'popia_text', 'label': 'Agreement: full text', 'multiline': True,
             'default': ('1. Communication Mandate\n'
                         'By submitting your phone number and email address through our general enquiry form, you consent to '
                         'ZuriKO Technologies contacting you regarding your enquiry, including service information and quotes.\n\n'
                         '2. Retention Limits\n'
                         'Contact records and message logs are kept for a maximum of 24 months to track general enquiry history, '
                         'after which records are anonymised or permanently deleted.'),
             'help': 'Carried over from the old popia_contact.json. Please have it reviewed against how enquiries are actually handled.'},
            {'key': 'success_heading', 'label': 'Confirmation heading (after sending)', 'default': 'Message received'},
            {'key': 'success_text', 'label': 'Confirmation text', 'default': 'Thank you. Our team will get back to you shortly.'},
        ],
        'collections': [],
    },
}

# Careers filter buttons. A job's department is matched (case-insensitively, by substring)
# against these keywords to decide which button it belongs under. Jobs that match nothing
# still show under "All" and get an extra "Other" button.
CAREER_FILTERS = [
    ('HR', ['human resources']),
    ('IT', ['information technology']),
    ('Marketing', ['marketing', 'social media', 'sales']),
    ('Finance', ['finance']),
    ('Ops', ['operations', 'customer support', 'supply chain', 'logistics']),
]


def department_group(department):
    d = (department or '').casefold()
    for group, keywords in CAREER_FILTERS:
        if any(k in d for k in keywords):
            return group
    return 'Other'


def block_config(page, key):
    cfg = PAGES.get(page)
    if not cfg:
        return None
    for block in cfg['blocks']:
        if block['key'] == key:
            return block
    return None


def default_for(page, key):
    """Default wording for a block, or '' if the page/key is unknown."""
    block = block_config(page, key)
    return block['default'] if block else ''
