import re

from django import template
from django.db import DatabaseError
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from dashboard.content import PAGES, default_for
from dashboard.models import ContentBlock, Record, ContactMessage, JobApplication

register = template.Library()


def _overrides_for(context, page):
    """Edited blocks for a page. Fetched once per request, not once per tag."""
    request = context.get('request')
    cache = None
    if request is not None:
        cache = getattr(request, '_content_block_cache', None)
        if cache is None:
            cache = request._content_block_cache = {}
        if page in cache:
            return cache[page]
    try:
        data = dict(ContentBlock.objects.filter(page=page).values_list('key', 'value'))
    except DatabaseError:
        # Table not migrated yet: fall back to the defaults instead of breaking the public site.
        data = {}
    if cache is not None:
        cache[page] = data
    return data


@register.simple_tag(takes_context=True)
def page_text(context, page, key):
    """
    Editable page text:  {% page_text 'home' 'hero_title' %}
    For multi-line text:  {% page_text 'about' 'intro' as intro %}{{ intro|with_media|linebreaksbr }}
    Output is HTML-escaped (both forms), so editors can't inject markup.
    """
    value = _overrides_for(context, page).get(key)
    if value is None or value == '':
        return default_for(page, key)
    return value


@register.simple_tag(takes_context=True)
def page_lines(context, page, key):
    """A multi-line block as a list of non-empty, trimmed lines:  {% page_lines 'home' 'hero_lines' as lines %}"""
    text = page_text(context, page, key)
    return [line.strip() for line in text.splitlines() if line.strip()]


@register.simple_tag(takes_context=True)
def page_media(context, page, key):
    """
    URL of the Media library image chosen for a slot, or '' if none is chosen (or it was deleted):
        {% page_media 'home' 'background' as bg %}{% if bg %}<img src="{{ bg }}">{% endif %}
    """
    raw = _overrides_for(context, page).get(key)
    if not raw:
        return ''
    try:
        pk = int(raw)
        record = Record.objects.filter(pk=pk).first()
    except (TypeError, ValueError, DatabaseError):
        return ''
    if record and record.image:
        return record.image.url
    return ''


MEDIA_TOKEN = re.compile(r'\[media:(\d+)\]')


@register.filter(needs_autoescape=True)
def with_media(value, autoescape=True):
    """
    Escape the text, then swap every [media:ID] for that Media library image.
    Use before linebreaksbr:  {{ text|with_media|linebreaksbr }}
    Unknown ids, or items without an image, are dropped silently.
    """
    text = str(conditional_escape(value) if autoescape else value)
    ids = {int(i) for i in MEDIA_TOKEN.findall(text)}
    if not ids:
        return mark_safe(text)
    try:
        records = Record.objects.in_bulk(ids)
    except DatabaseError:
        records = {}

    def replace(match):
        record = records.get(int(match.group(1)))
        if not record or not record.image:
            return ''
        return str(format_html(
            '<figure class="media-embed"><img src="{}" alt="{}" loading="lazy"><figcaption>{}</figcaption></figure>',
            record.image.url, record.title, record.title,
        ))

    return mark_safe(MEDIA_TOKEN.sub(replace, text))


@register.inclusion_tag('manage/_nav.html', takes_context=True)
def manage_nav(context):
    """Tab bar shown at the top of every /manage/ screen. Views pass `active` to highlight a tab."""
    try:
        unhandled = ContactMessage.objects.filter(handled=False).count()
        unhandled_applications = JobApplication.objects.filter(handled=False).count()
    except DatabaseError:
        unhandled = unhandled_applications = 0
    return {
        'active': context.get('active', ''),
        'pages': [{'slug': slug, 'label': cfg['label']} for slug, cfg in PAGES.items()],
        'unhandled': unhandled,
        'unhandled_applications': unhandled_applications,
    }
