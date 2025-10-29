"""
Test configuration and fixtures for BlogForge tests.
"""
import pytest
import tempfile
import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from authlib.integrations.flask_client import OAuth

from app import create_app
from app.models import db, User, Blog, Tag


@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    # Create test app with testing configuration
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask application."""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create a test user for authentication."""
    with app.app_context():
        user = User(
            google_sub='test-google-sub-123',
            email='test@example.com',
            name='Test User',
            avatar_url='https://example.com/avatar.jpg'
        )
        db.session.add(user)
        db.session.commit()
        # Return user ID instead of user object to avoid session issues
        return user.id


@pytest.fixture
def authenticated_client(client, test_user):
    """Create an authenticated test client."""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(test_user)
        sess['_fresh'] = True
    return client


@pytest.fixture
def sample_blog_data():
    """Sample blog data for testing."""
    return {
        'title': 'Test Blog Post',
        'description': 'This is a test blog description',
        'content': '# Test Content\n\nThis is test markdown content.'
    }


@pytest.fixture
def existing_blog(app, test_user):
    """Create an existing blog for duplicate title testing."""
    with app.app_context():
        blog = Blog(
            user_id=test_user,
            title='Existing Blog Post',
            slug='existing-blog-post',
            description='This is an existing blog',
            content_markdown='# Existing Content',
            is_published=True,
            published_at=datetime.utcnow()
        )
        db.session.add(blog)
        db.session.commit()
        return blog
