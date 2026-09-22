from django.core.validators import FileExtensionValidator
from django.db import models

from .storage import get_private_storage
from .validators import validate_cv_size, validate_cv_signature

# --- Core Record Model ---
class Record(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    show_in_gallery = models.BooleanField(
        default=True,
        help_text="Show this image in the About page gallery. Untick for logos and backgrounds.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# --- Dynamic Page Models ---
class Service(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, help_text="e.g., IT Services, Media, Construction")
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, help_text="Optional bootstrap icon class")
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.category}: {self.title}"

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Hybrid (Centurion based)")
    level = models.CharField(max_length=100, help_text="e.g., Senior, Junior (Internship)")
    scope = models.TextField()
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class ContentBlock(models.Model):
    """
    An edited piece of page text (see dashboard/content.py for the list of blocks and defaults).
    A row only exists while the text differs from the default; deleting it restores the default.
    """
    page = models.CharField(max_length=50)
    key = models.CharField(max_length=100)
    value = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['page', 'key']
        constraints = [
            models.UniqueConstraint(fields=['page', 'key'], name='unique_content_block_per_page'),
        ]

    def __str__(self):
        return f"{self.page}.{self.key}"



def _cells(line):
    return [c.strip() for c in line.split('|')]


class Division(models.Model):
    """One capability section on the About page (Division 01, 02, ...)."""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(help_text="Main paragraph. Type [media:ID] to place a media-library image inside the text.")
    bullets = models.TextField(blank=True, help_text="One capability per line.")
    stats = models.TextField(
        blank=True,
        help_text='One per line as "Value | Label", e.g.  Java & .NET Core | Ecosystem Focus',
    )
    comparison = models.TextField(
        blank=True,
        help_text='Comparison table. First line = column headings, then one row per line. Separate columns with " | ".',
    )
    media = models.ForeignKey(
        Record, null=True, blank=True, on_delete=models.SET_NULL, related_name='divisions',
        help_text="Optional image from the media library.",
    )
    order = models.IntegerField(default=0, help_text="Lower numbers appear first.")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def bullet_list(self):
        return [b.strip() for b in self.bullets.splitlines() if b.strip()]

    def stat_list(self):
        rows = []
        for line in self.stats.splitlines():
            if line.strip():
                cells = _cells(line)
                rows.append({'value': cells[0], 'label': cells[1] if len(cells) > 1 else ''})
        return rows

    def comparison_table(self):
        lines = [l for l in self.comparison.splitlines() if l.strip()]
        if not lines:
            return None
        return {'head': _cells(lines[0]), 'rows': [_cells(l) for l in lines[1:]]}


class ContactMessage(models.Model):
    """Enquiries sent through the Contact page form."""
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    popia_consent = models.BooleanField(default=False)
    handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"


class JobApplication(models.Model):
    """A candidate's application, submitted from a job's Apply page."""
    job = models.ForeignKey(JobPosting, null=True, blank=True, on_delete=models.SET_NULL, related_name='applications')
    role = models.CharField(max_length=200, help_text="The job title at the time of applying.")
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    message = models.TextField(blank=True)
    cv = models.FileField(
        upload_to='cvs/%Y/%m/', storage=get_private_storage,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx']), validate_cv_size, validate_cv_signature],
    )
    popia_consent = models.BooleanField(default=False)
    handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"

    def delete(self, *args, **kwargs):
        """Deleting an application also removes the stored CV file."""
        cv = self.cv
        result = super().delete(*args, **kwargs)
        if cv:
            cv.delete(save=False)
        return result
