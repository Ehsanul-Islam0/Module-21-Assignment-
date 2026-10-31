from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from portfolio_app.models import Category, Comment, ContactMessage, Education, Experience, Post, PostLike, Profile, Project, Skill, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the portfolio site with realistic demo data.'

    def handle(self, *args, **options):
        if User.objects.filter(username='owner').exists():
            self.stdout.write('Demo data already exists.')
            return

        user = User.objects.create_user(username='owner', email='owner@example.com', password='admin123', is_superuser=True, is_staff=True)

        Profile.objects.create(
            full_name='Md. Ehsanul Islam',
            headline='Full-Stack Developer',
            bio='I build thoughtful digital products and reliable backend systems for real-world problems.',
            email='md.ehsanul.islam@gmail.com',
            phone='+8801700000000',
            location='Dhaka, Bangladesh',
            github_url='https://github.com',
            linkedin_url='https://linkedin.com',
            x_url='https://x.com',
            website_url='https://example.com',
            years_of_experience=2,
            is_available_for_hire=True,
        )

        skills = [
            Skill.objects.create(name='React', category='FRONTEND', proficiency=92, display_order=1, is_featured=True),
            Skill.objects.create(name='Django', category='BACKEND', proficiency=94, display_order=2, is_featured=True),
            Skill.objects.create(name='TypeScript', category='FRONTEND', proficiency=88, display_order=3),
            Skill.objects.create(name='PostgreSQL', category='DATABASE', proficiency=82, display_order=4),
            Skill.objects.create(name='Docker', category='DEVOPS', proficiency=76, display_order=5),
            Skill.objects.create(name='REST APIs', category='BACKEND', proficiency=90, display_order=6),
            Skill.objects.create(name='Git', category='TOOLS', proficiency=86, display_order=7),
            Skill.objects.create(name='Communication', category='SOFT_SKILL', proficiency=84, display_order=8),
            Skill.objects.create(name='Node.js', category='BACKEND', proficiency=74, display_order=9),
            Skill.objects.create(name='Figma', category='TOOLS', proficiency=72, display_order=10),
        ]

        Experience.objects.create(
            company='Kreative Labs',
            role='Frontend Developer',
            employment_type='FULL_TIME',
            location='Remote',
            start_date='2024-01-01',
            end_date='2025-05-01',
            is_current=False,
            description='Built dashboard interfaces, internal tools, and product marketing pages that improved conversion and team clarity.',
            company_url='https://example.com',
            display_order=1,
        )
        Experience.objects.create(
            company='CodeCraft Studio',
            role='Full-Stack Engineer',
            employment_type='FREELANCE',
            location='Dhaka',
            start_date='2023-06-01',
            end_date=None,
            is_current=True,
            description='Helped founders design and launch SaaS MVPs, customer portals, and internal analytics workflows tailored to business needs.',
            company_url='https://example.com',
            display_order=2,
        )

        Education.objects.create(
            institution='University of Dhaka',
            degree='BSc in Computer Science',
            field_of_study='Computer Science and Engineering',
            start_year=2018,
            end_year=2022,
            grade='CGPA 3.7',
            description='Focused on software engineering, databases, networking, and human-computer interaction.',
        )

        cat1 = Category.objects.create(name='Web Development', slug='web-development', description='Frontend and backend product work.')
        cat2 = Category.objects.create(name='Product Design', slug='product-design', description='UX notes and interface thinking.')
        cat3 = Category.objects.create(name='Career', slug='career', description='Lessons and reflections from building a career.')

        tag1 = Tag.objects.create(name='React', slug='react')
        tag2 = Tag.objects.create(name='Django', slug='django')
        tag3 = Tag.objects.create(name='Portfolio', slug='portfolio')
        tag4 = Tag.objects.create(name='UX', slug='ux')
        tag5 = Tag.objects.create(name='Career', slug='career')
        tag6 = Tag.objects.create(name='APIs', slug='apis')

        project1 = Project.objects.create(
            title='Course Portal',
            slug='course-portal',
            summary='Learning dashboard for online courses.',
            description='A responsive platform for managing student learning journeys and course content.',
            cover_image='projects/course-portal.jpg',
            category='WEB',
            live_url='https://example.com',
            github_url='https://github.com',
            is_featured=True,
            completed_date='2024-09-01',
            display_order=1,
        )
        project2 = Project.objects.create(
            title='Inventory Manager',
            slug='inventory-manager',
            summary='Warehouse inventory and order tracking solution.',
            description='A streamlined dashboard for stock monitoring, product tracking, and business reporting.',
            cover_image='projects/inventory.jpg',
            category='API',
            live_url='https://example.com',
            github_url='https://github.com',
            is_featured=True,
            completed_date='2025-01-15',
            display_order=2,
        )
        project3 = Project.objects.create(
            title='Client CRM',
            slug='client-crm',
            summary='Lead pipeline and follow-up management tool.',
            description='A lightweight CRM built to support relationship tracking and reporting for small businesses.',
            cover_image='projects/crm.jpg',
            category='WEB',
            live_url='https://example.com',
            github_url='https://github.com',
            is_featured=False,
            completed_date='2023-12-10',
            display_order=3,
        )
        project1.tech_stack.set([skills[0], skills[1], skills[3]])
        project2.tech_stack.set([skills[1], skills[5], skills[3]])
        project3.tech_stack.set([skills[0], skills[6], skills[7]])

        post1 = Post.objects.create(
            title='How I Built My First Full-Stack Dashboard',
            slug='how-i-built-my-first-full-stack-dashboard',
            excerpt='A project diary on designing and shipping a thoughtful dashboard with React and Django.',
            content='This is a longer article about building a dashboard with React and Django, planning the API carefully, and designing interfaces that still feel intuitive after launch. I started by sketching the user journey and breaking the problem into small product goals. Then I mapped the data model, the API endpoints, and the key frontend interactions. I learned that a great feature is not just functionally correct; it also reduces decision fatigue and makes the work easier for real people.',
            cover_image='posts/post-1.jpg',
            category=cat1,
            author=user,
            status='PUBLISHED',
            published_at='2025-01-10T10:00:00Z',
            views_count=240,
            reading_time=5,
            is_featured=True,
        )
        post2 = Post.objects.create(
            title='Why Clean API Design Matters in Real Projects',
            slug='why-clean-api-design-matters',
            excerpt='A reflection on designing APIs that are easy to scale, document, and debug.',
            content='A clean API is not just about speed. It is about trust, clarity, and maintainability. When the app grows or requirements change, the API becomes the backbone of the product. I learned to keep resources predictable, validation clear, and failure messages readable so both the frontend team and future collaborators could reason about the system without confusion.',
            cover_image='posts/post-2.jpg',
            category=cat1,
            author=user,
            status='PUBLISHED',
            published_at='2024-12-15T09:00:00Z',
            views_count=180,
            reading_time=4,
            is_featured=True,
        )
        post3 = Post.objects.create(
            title='A Practical Guide to Writing Better Product Copy',
            slug='practical-guide-writing-better-product-copy',
            excerpt='Small ideas that make product experiences feel clearer, warmer, and more human.',
            content='Good product copy turns a good interface into a great one. It helps people understand what is happening, what they should do next, and why it matters. I started paying more attention to empty states, onboarding messages, and button labels. The result was not just a cleaner interface, but a calmer and more trustworthy experience for users.',
            cover_image='posts/post-3.jpg',
            category=cat2,
            author=user,
            status='PUBLISHED',
            published_at='2024-11-20T12:00:00Z',
            views_count=132,
            reading_time=4,
            is_featured=False,
        )
        post4 = Post.objects.create(
            title='My Notes on Building a Personal Brand',
            slug='my-notes-on-building-a-personal-brand',
            excerpt='How I shaped a professional story through projects, writing, and thoughtful design decisions.',
            content='A personal brand is not a slogan. It is the story you consistently communicate through your work and your writing. I focused on shipping small but real projects and documenting the process so people could understand how I think. That helped me feel more confident in interviews and gave people a smoother way to evaluate my work.',
            cover_image='posts/post-4.jpg',
            category=cat3,
            author=user,
            status='PUBLISHED',
            published_at='2024-10-03T08:00:00Z',
            views_count=90,
            reading_time=3,
            is_featured=False,
        )
        post5 = Post.objects.create(
            title='Draft: Improving Loader States in UI',
            slug='draft-improving-loader-states-in-ui',
            excerpt='Draft notes about micro-interactions and better loading feedback for interface design.',
            content='This is still a draft, but my goal is to document how loader states can improve trust without creating visual noise. I am collecting examples from dashboard and store flows to see how small loading cues can guide users without overwhelming them.',
            cover_image='posts/post-draft.jpg',
            category=cat2,
            author=user,
            status='DRAFT',
            views_count=0,
            reading_time=2,
            is_featured=False,
        )

        for post in [post1, post2, post3, post4]:
            post.tags.set([tag1, tag2, tag3])
        post5.tags.set([tag4, tag5])

        Comment.objects.create(post=post1, name='Rahim', email='rahim@example.com', content='This is a really practical write-up. I like the design decisions.', is_approved=True)
        Comment.objects.create(post=post1, name='Naila', email='naila@example.com', content='The API examples made the concept much easier to understand.', is_approved=True)
        Comment.objects.create(post=post2, name='Sadia', email='sadia@example.com', content='I think clean API design really matters. Helpful post!', is_approved=False)
        Comment.objects.create(post=post3, name='Tariq', email='tariq@example.com', content='Thanks for sharing your thoughts on product copy. Great breakdown.', is_approved=False)
        Comment.objects.create(post=post1, name='Ayan', email='ayan@example.com', content='This made me rethink my own dashboard structure.', is_approved=False)

        PostLike.objects.create(post=post1, visitor_id='visitor-1')
        PostLike.objects.create(post=post2, visitor_id='visitor-2')

        ContactMessage.objects.create(name='Fahad', email='fahad@example.com', subject='Project discussion', message='I would like to talk about a potential product collaboration.')
        ContactMessage.objects.create(name='Misha', email='misha@example.com', subject='Job enquiry', message='I saw your portfolio and would like to discuss a junior role opportunity.', is_read=True)

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
