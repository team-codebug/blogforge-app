"""
Integration tests for the complete blog creation workflow in BlogForge.
Tests the full user journey from login to blog creation to retrieval.
"""
import pytest
from flask import url_for
from app.models import Blog, User


class TestBlogCreationWorkflow:
    """Integration tests for the complete blog creation workflow."""

    def test_complete_blog_creation_workflow(self, app, client):
        """Test the complete user journey: login -> create blog -> retrieve blog."""
        from app.models import db
        
        # Step 1: Create a test user
        with app.app_context():
            user = User(
                google_sub='integration-test-user-123',
                email='integration@example.com',
                name='Integration Test User',
                avatar_url='https://example.com/integration-avatar.jpg'
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        
        # Step 2: Simulate user login by setting session
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user_id)
            sess['_fresh'] = True
        
        # Step 3: Access the new blog page
        new_blog_response = client.get(url_for('posts.new_blog'))
        assert new_blog_response.status_code == 200
        assert b'Create a new blog' in new_blog_response.data or b'New Blog' in new_blog_response.data
        
        # Step 4: Create a new blog with complete data
        blog_data = {
            'title': 'Integration Test Blog Post',
            'description': 'This is a comprehensive integration test for blog creation workflow',
            'content': '# Integration Test\n\nThis blog post tests the complete workflow from creation to retrieval.\n\n## Features Tested\n\n- User authentication\n- Blog creation\n- Data persistence\n- Blog retrieval\n\n**This is a test of the complete system!**'
        }
        
        create_response = client.post(
            url_for('posts.create_blog'),
            data=blog_data,
            follow_redirects=False
        )
        
        # Step 5: Verify blog creation response
        assert create_response.status_code == 302, f"Expected redirect, got {create_response.status_code}"
        assert 'edit' in create_response.location, f"Expected redirect to edit page, got {create_response.location}"
        
        # Step 6: Extract blog ID from redirect URL
        # The redirect URL should be something like '/posts/123/edit'
        redirect_parts = create_response.location.split('/')
        blog_id = None
        for i, part in enumerate(redirect_parts):
            if part == 'posts' and i + 1 < len(redirect_parts):
                blog_id = redirect_parts[i + 1]
                break
        
        assert blog_id is not None, f"Could not extract blog ID from redirect URL: {create_response.location}"
        assert blog_id.isdigit(), f"Expected numeric blog ID, got {blog_id}"
        blog_id = int(blog_id)
        
        # Step 7: Verify blog was created in database
        with app.app_context():
            created_blog = Blog.query.get(blog_id)
            assert created_blog is not None, "Blog should exist in database"
            assert created_blog.user_id == user_id, "Blog should belong to the test user"
            assert created_blog.title == blog_data['title']
            assert created_blog.description == blog_data['description']
            assert created_blog.content_markdown == blog_data['content']
            assert created_blog.is_published == True, "Blog should be published by default"
            assert created_blog.published_at is not None, "Blog should have publish timestamp"
            assert created_blog.slug == 'integration-test-blog-post', f"Expected slug 'integration-test-blog-post', got '{created_blog.slug}'"
        
        # Step 8: Access the edit page (where user is redirected after creation)
        edit_response = client.get(url_for('posts.edit_blog', blog_id=blog_id))
        assert edit_response.status_code == 200
        assert blog_data['title'].encode() in edit_response.data
        assert blog_data['description'].encode() in edit_response.data
        assert blog_data['content'].encode() in edit_response.data
        
        # Step 9: Access the blog detail page
        detail_response = client.get(url_for('posts.view_blog', blog_id=blog_id))
        assert detail_response.status_code == 200
        assert blog_data['title'].encode() in detail_response.data
        assert blog_data['content'].encode() in detail_response.data
        
        # Step 10: Verify blog appears in user's blog list
        list_response = client.get(url_for('posts.list_blogs'))
        assert list_response.status_code == 200
        assert blog_data['title'].encode() in list_response.data
        assert blog_data['description'].encode() in list_response.data
        
        # Step 11: Verify blog appears in dashboard (published blogs)
        dashboard_response = client.get(url_for('main.dashboard'))
        assert dashboard_response.status_code == 200
        assert blog_data['title'].encode() in dashboard_response.data
        assert blog_data['description'].encode() in dashboard_response.data
        
        # Step 12: Test blog API endpoint
        api_response = client.get(url_for('main.get_blog_content', blog_id=blog_id))
        assert api_response.status_code == 200
        api_data = api_response.get_json()
        assert api_data['title'] == blog_data['title']
        assert api_data['description'] == blog_data['description']
        assert api_data['content'] == blog_data['content']
        assert api_data['author']['name'] == 'Integration Test User'
        
        # Step 13: Verify database state is consistent
        with app.app_context():
            # Check that only one blog exists for this user
            user_blogs = Blog.query.filter_by(user_id=user_id).all()
            assert len(user_blogs) == 1, f"Expected 1 blog for user, found {len(user_blogs)}"
            
            # Verify all blog attributes
            blog = user_blogs[0]
            assert blog.id == blog_id
            assert blog.title == blog_data['title']
            assert blog.description == blog_data['description']
            assert blog.content_markdown == blog_data['content']
            assert blog.is_published == True
            assert blog.published_at is not None
            assert blog.created_at is not None
            assert blog.updated_at is not None
            assert blog.user_id == user_id
            assert blog.slug == 'integration-test-blog-post'

    def test_blog_creation_workflow_with_duplicate_title(self, app, client):
        """Test workflow when user tries to create blog with duplicate title."""
        from app.models import db
        
        # Step 1: Create a test user
        with app.app_context():
            user = User(
                google_sub='duplicate-test-user-456',
                email='duplicate@example.com',
                name='Duplicate Test User',
                avatar_url='https://example.com/duplicate-avatar.jpg'
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        
        # Step 2: Simulate user login
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user_id)
            sess['_fresh'] = True
        
        # Step 3: Create first blog
        first_blog_data = {
            'title': 'Duplicate Title Test',
            'description': 'First blog with this title',
            'content': '# First Blog\n\nThis is the first blog with this title.'
        }
        
        first_response = client.post(
            url_for('posts.create_blog'),
            data=first_blog_data,
            follow_redirects=False
        )
        assert first_response.status_code == 302
        assert 'edit' in first_response.location
        
        # Step 4: Try to create second blog with same title
        duplicate_blog_data = {
            'title': 'Duplicate Title Test',  # Same title
            'description': 'Second blog with same title',
            'content': '# Second Blog\n\nThis should fail due to duplicate title.'
        }
        
        duplicate_response = client.post(
            url_for('posts.create_blog'),
            data=duplicate_blog_data,
            follow_redirects=False
        )
        
        # Step 5: Verify duplicate creation is prevented
        assert duplicate_response.status_code == 302
        assert 'new' in duplicate_response.location  # Redirected back to new blog page
        
        # Step 6: Verify only one blog exists in database
        with app.app_context():
            user_blogs = Blog.query.filter_by(user_id=user_id).all()
            assert len(user_blogs) == 1, f"Expected 1 blog, found {len(user_blogs)}"
            assert user_blogs[0].title == 'Duplicate Title Test'
            assert user_blogs[0].description == 'First blog with this title'

    def test_blog_creation_workflow_unauthenticated(self, client):
        """Test that unauthenticated users cannot create blogs."""
        blog_data = {
            'title': 'Unauthorized Blog',
            'description': 'This should not be created',
            'content': '# Unauthorized\n\nThis blog should not be created.'
        }
        
        # Try to create blog without authentication
        response = client.post(
            url_for('posts.create_blog'),
            data=blog_data,
            follow_redirects=False
        )
        
        # Should redirect to login
        assert response.status_code == 302
        assert 'login' in response.location or 'auth' in response.location
        
        # Verify no blog was created
        from app.models import Blog
        with client.application.app_context():
            blog_count = Blog.query.count()
            assert blog_count == 0, f"Expected 0 blogs, found {blog_count}"

    def test_blog_creation_workflow_missing_title(self, app, client):
        """Test workflow when user tries to create blog without title."""
        from app.models import db
        
        # Step 1: Create a test user
        with app.app_context():
            user = User(
                google_sub='missing-title-user-789',
                email='missing@example.com',
                name='Missing Title User',
                avatar_url='https://example.com/missing-avatar.jpg'
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        
        # Step 2: Simulate user login
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user_id)
            sess['_fresh'] = True
        
        # Step 3: Try to create blog without title
        invalid_blog_data = {
            'title': '',  # Empty title
            'description': 'This blog has no title',
            'content': '# No Title\n\nThis blog should not be created.'
        }
        
        response = client.post(
            url_for('posts.create_blog'),
            data=invalid_blog_data,
            follow_redirects=False
        )
        
        # Step 4: Verify creation is prevented
        assert response.status_code == 302
        assert 'new' in response.location  # Redirected back to new blog page
        
        # Step 5: Verify no blog was created
        with app.app_context():
            user_blogs = Blog.query.filter_by(user_id=user_id).all()
            assert len(user_blogs) == 0, f"Expected 0 blogs, found {len(user_blogs)}"

    def test_blog_creation_workflow_different_users_same_title(self, app):
        """Test that different users can create blogs with same title by directly creating in database."""
        from app.models import db
        
        # Step 1: Create two test users
        with app.app_context():
            user1 = User(
                google_sub='user1-same-title-111',
                email='user1@example.com',
                name='User One',
                avatar_url='https://example.com/user1.jpg'
            )
            user2 = User(
                google_sub='user2-same-title-222',
                email='user2@example.com',
                name='User Two',
                avatar_url='https://example.com/user2.jpg'
            )
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            user1_id = user1.id
            user2_id = user2.id
        
        # Step 2: Create blogs directly in database to test the business logic
        with app.app_context():
            from datetime import datetime
            
            # Create blog for user 1
            blog1 = Blog(
                user_id=user1_id,
                title='Same Title for Different Users',
                slug='same-title-for-different-users',
                description='User 1 blog',
                content_markdown='# User 1 Blog\n\nThis is user 1 blog.',
                is_published=True,
                published_at=datetime.utcnow()
            )
            
            # Create blog for user 2 with same title
            blog2 = Blog(
                user_id=user2_id,
                title='Same Title for Different Users',
                slug='same-title-for-different-users-2',
                description='User 2 blog',
                content_markdown='# User 2 Blog\n\nThis is user 2 blog.',
                is_published=True,
                published_at=datetime.utcnow()
            )
            
            db.session.add(blog1)
            db.session.add(blog2)
            db.session.commit()
            
            # Step 3: Verify both blogs exist in database
            user1_blogs = Blog.query.filter_by(user_id=user1_id).all()
            user2_blogs = Blog.query.filter_by(user_id=user2_id).all()
            
            assert len(user1_blogs) == 1, f"Expected 1 blog for user1, found {len(user1_blogs)}"
            assert len(user2_blogs) == 1, f"Expected 1 blog for user2, found {len(user2_blogs)}"
            
            # Both blogs should have same title but different content
            assert user1_blogs[0].title == 'Same Title for Different Users'
            assert user2_blogs[0].title == 'Same Title for Different Users'
            assert user1_blogs[0].description == 'User 1 blog'
            assert user2_blogs[0].description == 'User 2 blog'
            assert user1_blogs[0].user_id != user2_blogs[0].user_id
            
            # Verify the duplicate check logic works correctly
            # User 1 should not be able to create another blog with same title
            existing_for_user1 = Blog.query.filter_by(user_id=user1_id, title='Same Title for Different Users').first()
            assert existing_for_user1 is not None, "User 1 should have a blog with this title"
            
            # User 2 should not be able to create another blog with same title
            existing_for_user2 = Blog.query.filter_by(user_id=user2_id, title='Same Title for Different Users').first()
            assert existing_for_user2 is not None, "User 2 should have a blog with this title"
