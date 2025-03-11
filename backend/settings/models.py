from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    site_description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    primary_color = models.CharField(max_length=20, blank=True, null=True)
    accent_color = models.CharField(max_length=20, blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)
    meta_tags = models.JSONField(blank=True, null=True)
    analytics_id = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name_plural = 'Site Settings'