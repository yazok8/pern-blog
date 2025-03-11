from django.core.management.base import BaseCommand
from accounts.models import User
from content.models import Category, Article, ArticleCategory, Post

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            email='seed@example.com',
            defaults={
                'name': 'Seed User',
                'password': 'password123',  # In production, use set_password()
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created new user'))
        else:
            self.stdout.write('Using existing user')
            
        # Create categories
        categories = [
            {'name': 'Chronic Pain', 'slug': 'chronic-pain', 'description': 'Mind and body health related articles'},
            {'name': 'Mental Health', 'slug': 'mental-health', 'description': 'Mental health related articles'},
            {'name': 'ADHD', 'slug': 'adhd', 'description': 'ADHD related articles'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            
        # Create multiple articles (tips)
        articles_data = [
            {
                'slug': '3-supplements-that-helped-me',
                'defaults': {
                    'title': '3 Supplements That Helped Me',
                    'content': (
                        '1. Magnesium - Calmed my nerves after tough days...\n'
                        '2. Vitamin D - Boosted my mood in Canada\'s winters...\n'
                        '3. Omega-3 - Enhanced my focus and improved my depression...'
                    ),
                    'excerpt': 'Simple supplements that eased my chronic pain.',
                    'published': True,
                    'author': user,
                }
            },
            {
                'slug': 'healthy-habits-for-daily-life',
                'defaults': {
                    'title': 'Healthy Habits for Daily Life',
                    'content': (
                        '1. Exercise regularly.\n'
                        '2. Sleep at least 7-8 hours a night.\n'
                        '3. Eat a balanced diet rich in fruits and vegetables.'
                    ),
                    'excerpt': 'Daily habits that help maintain a healthy lifestyle.',
                    'published': True,
                    'author': user,
                }
            },
            {
                'slug': 'mindfulness-for-stress-management',
                'defaults': {
                    'title': 'Mindfulness for Stress Management',
                    'content': (
                        'Practicing mindfulness meditation daily can significantly reduce stress levels '
                        'and improve focus.'
                    ),
                    'excerpt': 'A guide to using mindfulness to manage stress effectively.',
                    'published': True,
                    'author': user,
                }
            },
        ]
        
        for article_data in articles_data:
            article, created = Article.objects.get_or_create(
                slug=article_data['slug'],
                defaults=article_data['defaults']
            )
            if created:
                # Optionally assign categories to article if needed using your through model
                for cat in Category.objects.all():
                    ArticleCategory.objects.get_or_create(article=article, category=cat)
                self.stdout.write(self.style.SUCCESS(f'Created article: {article.title}'))
            else:
                self.stdout.write(f'Using existing article: {article.title}')
        
        # Create posts data
        posts_data = [
            {
                'slug': 'question-about-supplements',
                'defaults': {
                    'title': 'Which Supplements Work Best for Pain?',
                    'content': (
                        'Hi everyone! I’ve been struggling with chronic back pain and am curious about '
                        'supplements that have worked for others. I’ve tried magnesium, but no luck yet. '
                        'Any suggestions?'
                    ),
                    'excerpt': 'Seeking advice on supplements for chronic back pain.',
                    'published': False,  # Requires moderation
                    'author': user,
                    'content_type': 'STANDARD',
                }
            },
            {
                'slug': 'meditation-success-story',
                'defaults': {
                    'title': 'My Meditation Journey',
                    'content': (
                        'After months of stress from fibromyalgia, I started meditating 10 minutes daily. '
                        'It’s reduced my pain flare-ups significantly! Anyone else try this?'
                    ),
                    'excerpt': 'Sharing how meditation helped with fibromyalgia pain.',
                    'published': False,  # Requires moderation
                    'author': user,
                    'content_type': 'STANDARD',
                }
            },
            {
                'slug': 'omega-3-experience',
                'defaults': {
                    'title': 'Omega-3 Changed My Life',
                    'content': (
                        'I started taking omega-3 supplements for joint pain, and after two months, '
                        'I noticed a big difference. Has anyone else had similar results?'
                    ),
                    'excerpt': 'Experience with omega-3 for joint pain relief.',
                    'published': False,  # Requires moderation
                    'author': user,
                    'content_type': 'STANDARD',
                }
            },
        ]
        
        for post_data in posts_data:
            post, created = Post.objects.get_or_create(
                slug=post_data['slug'],
                defaults=post_data['defaults']
            )
            if created:
                # Optionally assign a category (e.g., Chronic Pain)
                try:
                    category = Category.objects.get(slug='chronic-pain')
                    post.categories.add(category)
                except Category.DoesNotExist:
                    self.stdout.write('Category "chronic-pain" does not exist.')
                self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))
            else:
                self.stdout.write(f'Using existing post: {post.title}')
                
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
