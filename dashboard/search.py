"""
Site-wide search.

- Case-insensitive (casefold), and every word in the query must appear (so "java developer" finds "Senior Java Developer").
- Searches the wording of the public pages (including edits made in /manage/), services, job postings,
  FAQs, About divisions and the media library.
- Each result carries a URL that lands on the right page and scrolls to / highlights the match:
      /services/?hl=cyber#service-8      (the page's JavaScript reads ?hl= and the #anchor)
"""
import re
from urllib.parse import urlencode

from django.db import DatabaseError
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .content import PAGES
from .models import ContentBlock, Service, JobPosting, Faq, Division, Record

MIN_LENGTH = 2
SNIPPET_RADIUS = 90

KIND_ORDER = ['Page', 'Service', 'Division', 'Job', 'FAQ', 'Media']


def _terms(query):
    seen, terms = set(), []
    for word in query.split():
        folded = word.casefold()
        if len(folded) >= 1 and folded not in seen:
            seen.add(folded)
            terms.append(folded)
    return terms


def _matches(text, terms):
    hay = (text or '').casefold()
    return all(t in hay for t in terms)


def _score(title, terms):
    """Title matches rank above body-only matches."""
    return 2 if _matches(title, terms) else 1


def _url(name, query, anchor='', **kwargs):
    url = reverse(name, kwargs=kwargs or None)
    url += '?' + urlencode({'hl': query})
    return url + (f'#{anchor}' if anchor else '')


def highlight(text, terms):
    """HTML-escape `text` and wrap every match of any term in <mark>. Safe to render."""
    if not terms:
        return mark_safe(escape(text))
    pattern = re.compile('(' + '|'.join(re.escape(t) for t in sorted(terms, key=len, reverse=True)) + ')', re.IGNORECASE)
    pieces = pattern.split(text)
    out = []
    for i, piece in enumerate(pieces):
        out.append(f'<mark>{escape(piece)}</mark>' if i % 2 else escape(piece))
    return mark_safe(''.join(out))


def snippet(text, terms):
    """A short excerpt around the first match, with matches highlighted."""
    text = ' '.join((text or '').split())
    folded = text.casefold()
    positions = [folded.find(t) for t in terms if folded.find(t) >= 0]
    start = max(min(positions) - SNIPPET_RADIUS, 0) if positions else 0
    excerpt = text[start:start + SNIPPET_RADIUS * 2 + 40]
    prefix = '…' if start > 0 else ''
    suffix = '…' if start + len(excerpt) < len(text) else ''
    return mark_safe(prefix + highlight(excerpt, terms) + suffix)


def _effective_text(page_slug):
    """(block, current text) for every text block on a page: the edit if there is one, else the default."""
    try:
        overrides = dict(ContentBlock.objects.filter(page=page_slug).values_list('key', 'value'))
    except DatabaseError:
        overrides = {}
    for block in PAGES[page_slug]['blocks']:
        if block.get('type') == 'media':
            continue
        yield block, (overrides.get(block['key']) or block['default'])


def run_search(query):
    """Return a list of result dicts, best first. Empty if the query is too short."""
    query = (query or '').strip()
    if len(query) < MIN_LENGTH:
        return []
    terms = _terms(query)
    results = []

    def add(kind, title, url, body, page_label, score):
        results.append({
            'kind': kind, 'title': title, 'url': url, 'page': page_label,
            'snippet': snippet(body, terms), 'score': score,
        })

    # 1) Wording of the public pages: one result per page (its best-matching block).
    for slug, cfg in PAGES.items():
        if slug == 'site':
            continue
        best = None
        for block, text in _effective_text(slug):
            if text and _matches(text, terms):
                candidate = (2 if block['key'] == 'heading' else 1, text)
                if best is None or candidate[0] > best[0]:
                    best = candidate
        if best:
            add('Page', f"{cfg['label']} page", _url(cfg['url_name'], query), best[1], cfg['label'], best[0])

    # 2) Lists
    for s in Service.objects.all():
        blob = f"{s.title} {s.category} {s.description}"
        if _matches(blob, terms):
            add('Service', s.title, _url('services', query, f'service-{s.pk}'),
                f"{s.category}. {s.description}", 'Services', _score(s.title, terms))

    for d in Division.objects.all():
        blob = ' '.join([d.title, d.subtitle, d.description, d.bullets, d.stats, d.comparison])
        if _matches(blob, terms):
            body = d.description if _matches(d.description, terms) else (d.subtitle or d.description)
            add('Division', d.title, _url('about', query, f'division-{d.pk}'), body, 'About', _score(d.title, terms))

    for j in JobPosting.objects.filter(is_active=True):
        blob = ' '.join([j.title, j.department, j.location, j.level, j.scope, j.requirements])
        if _matches(blob, terms):
            add('Job', j.title, _url('careers', query, f'job-{j.pk}'),
                f"{j.department} · {j.level}. {j.scope}", 'Careers', _score(j.title, terms))

    for f in Faq.objects.all():
        if _matches(f"{f.question} {f.answer}", terms):
            body = f.answer if not _matches(f.question, terms) else f.question
            add('FAQ', f.question, _url('about', query, f'faq-{f.pk}'), body, 'About', _score(f.question, terms))

    for r in Record.objects.all():
        if _matches(f"{r.title} {r.description}", terms):
            url = reverse('record_detail', kwargs={'pk': r.pk})
            add('Media', r.title, url, r.description or r.title, 'Media library', _score(r.title, terms))

    results.sort(key=lambda r: (-r['score'], KIND_ORDER.index(r['kind'])))
    return results
