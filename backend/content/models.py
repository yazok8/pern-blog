from django.db import models
from django.utils.text import slugify
from accounts.models import User

# -------------------------------------------------------------------
# Category and Tag Models
# -------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# -------------------------------------------------------------------
# Post Model (for simple blog posts)
# -------------------------------------------------------------------
class Post(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('STANDARD', 'Standard'),
        ('FEATURED', 'Featured'),
        ('PINNED', 'Pinned'),
        ('SPONSORED', 'Sponsored'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    # Many-to-many relationship for additional categories.
    categories = models.ManyToManyField(
        Category, 
        related_name='post_categories'
    )
    tags = models.ManyToManyField(
        Tag, 
        related_name='post_tags'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(blank=True, null=True)  # in minutes
    content_type = models.CharField(
        max_length=20, 
        choices=CONTENT_TYPE_CHOICES, 
        default='STANDARD'
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.reading_time:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 250))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# -------------------------------------------------------------------
# Article Model (for feature-rich articles)
# -------------------------------------------------------------------
class Article(models.Model):
    ARTICLE_TYPE_CHOICES = [
        ('STANDARD', 'Standard'),
        ('INTERVIEW', 'Interview'),
        ('TUTORIAL', 'Tutorial'),
        ('REVIEW', 'Review'),
        ('OPINION', 'Opinion'),
        ('ANALYSIS', 'Analysis'),
        ('NEWS', 'News'),
        ('CASE_STUDY', 'Case Study'),
        ('RESEARCH', 'Research'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    external_link = models.URLField(blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='articles'
    )
    # Primary category: single main category selection.
    primary_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_articles'
    )
    # Additional categories via a many-to-many relationship with a through model.
    categories = models.ManyToManyField(
        Category, 
        through='ArticleCategory',
        related_name='article_categories'
    )
    tags = models.ManyToManyField(
        Tag,
        through='ArticleTag',
        related_name='article_tags'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(
        max_length=20, 
        choices=ARTICLE_TYPE_CHOICES, 
        default='STANDARD'
    )
    is_sponsored = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    seo_meta = models.JSONField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    cover_design = models.ImageField(upload_to='covers/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.reading_time:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 250))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# -------------------------------------------------------------------
# Through Models for Article Categories and Tags
# -------------------------------------------------------------------
class ArticleCategory(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('article', 'category')
    
    def __str__(self):
        return f"{self.article.title} - {self.category.name}"


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('article', 'tag')
    
    def __str__(self):
        return f"{self.article.title} - {self.tag.name}"


# -------------------------------------------------------------------
# Comment, Like, and ArticleLike Models
# -------------------------------------------------------------------
class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        null=True, 
        blank=True
    )
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        null=True, 
        blank=True
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='replies', 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.author.name} on {self.created_at.strftime('%Y-%m-%d')}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.user.name} likes {self.post.title}"


class ArticleLike(models.Model):
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='article_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('article', 'user')
    
    def __str__(self):
        return f"{self.user.name} likes {self.article.title}"
