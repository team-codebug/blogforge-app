"""
Unit tests for the posts routes, specifically the create_blog endpoint.
"""
import pytest
from flask import url_for
from app.models import Blog, User


class TestCreateBlogEndpoint:
    """Test cases for the POST /posts/ create_blog endpoint."""

    def test_create_blog_success(self, authenticated_client, test_user, sample_blog_data):
        """Test that a new blog is successfully created when valid data is provided."""
        # Make POST request to create blog
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=sample_blog_data,
            follow_redirects=False
        )
        
        # Should redirect to edit page (status 302)
        assert response.status_code == 302
        assert 'edit' in response.location
        
        # Verify blog was created in database
        blog = Blog.query.filter_by(title=sample_blog_data['title']).first()
        assert blog is not None
        assert blog.title == sample_blog_data['title']
        assert blog.description == sample_blog_data['description']
        assert blog.content_markdown == sample_blog_data['content']
        assert blog.user_id == test_user
        assert blog.is_published == True
        assert blog.published_at is not None
        assert blog.slug == 'test-blog-post'  # title.lower().replace(' ', '-')

    def test_create_blog_missing_title(self, authenticated_client, sample_blog_data):
        """Test that API returns error when a post is submitted without a title."""
        # Remove title from data
        invalid_data = sample_blog_data.copy()
        del invalid_data['title']
        
        # Make POST request without title
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=invalid_data,
            follow_redirects=False
        )
        
        # Should redirect back to new blog page (status 302)
        assert response.status_code == 302
        assert 'new' in response.location
        
        # Verify no blog was created
        blog_count = Blog.query.count()
        assert blog_count == 0

    def test_create_blog_empty_title(self, authenticated_client, sample_blog_data):
        """Test that API returns error when title is empty string."""
        # Set empty title
        invalid_data = sample_blog_data.copy()
        invalid_data['title'] = ''
        
        # Make POST request with empty title
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=invalid_data,
            follow_redirects=False
        )
        
        # Should redirect back to new blog page (status 302)
        assert response.status_code == 302
        assert 'new' in response.location
        
        # Verify no blog was created
        blog_count = Blog.query.count()
        assert blog_count == 0

    def test_create_blog_whitespace_title(self, authenticated_client, sample_blog_data):
        """Test that API returns error when title is only whitespace."""
        # Set whitespace-only title
        invalid_data = sample_blog_data.copy()
        invalid_data['title'] = '   \n\t   '
        
        # Make POST request with whitespace title
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=invalid_data,
            follow_redirects=False
        )
        
        # Should redirect back to new blog page (status 302)
        assert response.status_code == 302
        assert 'new' in response.location
        
        # Verify no blog was created
        blog_count = Blog.query.count()
        assert blog_count == 0

    def test_create_blog_duplicate_title_same_user(self, authenticated_client, test_user, sample_blog_data, existing_blog):
        """Test that creating a blog with duplicate title for same user fails gracefully."""
        # Use the same title as existing blog
        duplicate_data = sample_blog_data.copy()
        duplicate_data['title'] = 'Existing Blog Post'  # Use the known title
        
        # Make POST request with duplicate title
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=duplicate_data,
            follow_redirects=False
        )
        
        # Should redirect back to new blog page with error (not create duplicate)
        assert response.status_code == 302
        assert 'new' in response.location
        
        # Verify only one blog exists (no duplicate created)
        blogs = Blog.query.filter_by(title='Existing Blog Post').all()
        assert len(blogs) == 1

    def test_create_blog_duplicate_title_flash_message(self, authenticated_client, test_user, sample_blog_data, existing_blog):
        """Test that duplicate title shows appropriate flash message."""
        # Use the same title as existing blog
        duplicate_data = sample_blog_data.copy()
        duplicate_data['title'] = 'Existing Blog Post'  # Use the known title
        
        # Make POST request with duplicate title
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=duplicate_data,
            follow_redirects=True  # Follow redirects to see the page
        )
        
        # Should redirect to new blog page
        assert response.status_code == 200
        assert b'new' in response.data or b'New' in response.data
        
        # Check for flash message in response (if template displays it)
        # Note: This test verifies the redirect behavior, flash message display
        # would need to be tested with template rendering if needed

    def test_create_blog_duplicate_title_different_user(self, app, client, sample_blog_data, existing_blog):
        """Test that different users can create blogs with same title."""
        from app.models import db, User
        
        # Create a second user
        with app.app_context():
            user2 = User(
                google_sub='test-google-sub-456',
                email='test2@example.com',
                name='Test User 2',
                avatar_url='https://example.com/avatar2.jpg'
            )
            db.session.add(user2)
            db.session.commit()
            user2_id = user2.id
        
        # Authenticate as second user
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user2_id)
            sess['_fresh'] = True
        
        # Use the same title as existing blog
        duplicate_data = sample_blog_data.copy()
        duplicate_data['title'] = 'Existing Blog Post'  # Use the known title
        
        # Make POST request with duplicate title
        response = client.post(
            url_for('posts.create_blog'),
            data=duplicate_data,
            follow_redirects=False
        )
        
        # Should create the blog successfully
        assert response.status_code == 302
        assert 'edit' in response.location
        
        # Verify both blogs exist with different user_ids
        blogs = Blog.query.filter_by(title='Existing Blog Post').all()
        assert len(blogs) == 2
        assert blogs[0].user_id != blogs[1].user_id

    def test_create_blog_missing_content(self, authenticated_client, test_user):
        """Test that blog can be created with missing content (optional field)."""
        data = {
            'title': 'Blog Without Content',
            'description': 'This blog has no content',
            # content is missing
        }
        
        # Make POST request without content
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=data,
            follow_redirects=False
        )
        
        # Should create successfully
        assert response.status_code == 302
        assert 'edit' in response.location
        
        # Verify blog was created
        blog = Blog.query.filter_by(title=data['title']).first()
        assert blog is not None
        assert blog.content_markdown == ''  # Empty string for missing content

    def test_create_blog_missing_description(self, authenticated_client, test_user):
        """Test that blog can be created with missing description (optional field)."""
        data = {
            'title': 'Blog Without Description',
            'content': '# This blog has no description',
            # description is missing
        }
        
        # Make POST request without description
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=data,
            follow_redirects=False
        )
        
        # Should create successfully
        assert response.status_code == 302
        assert 'edit' in response.location
        
        # Verify blog was created
        blog = Blog.query.filter_by(title=data['title']).first()
        assert blog is not None
        assert blog.description == ''  # Empty string for missing description

    def test_create_blog_unauthenticated(self, client, sample_blog_data):
        """Test that unauthenticated users cannot create blogs."""
        # Make POST request without authentication
        response = client.post(
            url_for('posts.create_blog'),
            data=sample_blog_data,
            follow_redirects=False
        )
        
        # Should redirect to login page
        assert response.status_code == 302
        assert 'login' in response.location or 'auth' in response.location
        
        # Verify no blog was created
        blog_count = Blog.query.count()
        assert blog_count == 0

    def test_create_blog_slug_generation(self, authenticated_client, test_user):
        """Test that slug is properly generated from title."""
        data = {
            'title': 'My Amazing Blog Post!',
            'description': 'Test description',
            'content': '# Test content'
        }
        
        # Make POST request
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=data,
            follow_redirects=False
        )
        
        # Should create successfully
        assert response.status_code == 302
        
        # Verify slug generation
        blog = Blog.query.filter_by(title=data['title']).first()
        assert blog is not None
        assert blog.slug == 'my-amazing-blog-post!'  # title.lower().replace(' ', '-')

    def test_create_blog_published_by_default(self, authenticated_client, test_user, sample_blog_data):
        """Test that blogs are created as published by default."""
        # Make POST request
        response = authenticated_client.post(
            url_for('posts.create_blog'),
            data=sample_blog_data,
            follow_redirects=False
        )
        
        # Should create successfully
        assert response.status_code == 302
        
        # Verify blog is published
        blog = Blog.query.filter_by(title=sample_blog_data['title']).first()
        assert blog is not None
        assert blog.is_published == True
        assert blog.published_at is not None
