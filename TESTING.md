# BlogForge Testing Guide

## Overview

This document describes the testing setup and test cases for the BlogForge platform, specifically focusing on the `/create-post` API endpoint.

## Test Framework

- **pytest**: Main testing framework
- **pytest-flask**: Flask-specific testing utilities
- **pytest-cov**: Code coverage reporting

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Test fixtures and configuration
└── test_posts_routes.py     # Unit tests for posts routes
```

## Running Tests

### Prerequisites

1. Ensure virtual environment is activated:
   ```bash
   source .venv/bin/activate
   ```

2. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running All Tests

```bash
./run_tests.sh
```

### Running Specific Test Categories

```bash
# Run only posts route tests
./run_tests.sh posts

# Run only unit tests
./run_tests.sh unit

# Run with verbose output
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=app --cov-report=html
```

## Test Cases for Create Blog Endpoint

### 1. Valid Blog Creation ✅

**Test**: `test_create_blog_success`

**Scenario**: A new blog is successfully created when valid data (title, content, and description) is provided.

**Expected Behavior**:
- HTTP 302 redirect to edit page
- Blog created in database with correct attributes
- Blog marked as published by default
- Slug generated from title

### 2. Missing Title Error ❌

**Test**: `test_create_blog_missing_title`

**Scenario**: The API returns error when a post is submitted without a title.

**Expected Behavior**:
- HTTP 302 redirect back to new blog page
- No blog created in database

### 3. Empty Title Error ❌

**Test**: `test_create_blog_empty_title`

**Scenario**: The API returns error when title is an empty string.

**Expected Behavior**:
- HTTP 302 redirect back to new blog page
- No blog created in database

### 4. Whitespace Title Error ❌

**Test**: `test_create_blog_whitespace_title`

**Scenario**: The API returns error when title contains only whitespace.

**Expected Behavior**:
- HTTP 302 redirect back to new blog page
- No blog created in database

### 5. Duplicate Title Handling 🔄

**Test**: `test_create_blog_duplicate_title_same_user`

**Scenario**: Attempting to create a post with duplicate title should be handled gracefully.

**Expected Behavior**:
- Currently allows duplicate titles (documents current behavior)
- Both blogs exist in database
- Each blog has unique ID

### 6. Cross-User Duplicate Titles ✅

**Test**: `test_create_blog_duplicate_title_different_user`

**Scenario**: Different users can create blogs with the same title.

**Expected Behavior**:
- Both blogs created successfully
- Different user_ids for each blog

### 7. Optional Fields Handling ✅

**Tests**: 
- `test_create_blog_missing_content`
- `test_create_blog_missing_description`

**Scenario**: Blog can be created with missing optional fields.

**Expected Behavior**:
- Blog created successfully
- Missing fields set to empty strings

### 8. Authentication Required 🔐

**Test**: `test_create_blog_unauthenticated`

**Scenario**: Unauthenticated users cannot create blogs.

**Expected Behavior**:
- HTTP 302 redirect to login page
- No blog created in database

### 9. Slug Generation 🔗

**Test**: `test_create_blog_slug_generation`

**Scenario**: Slug is properly generated from title.

**Expected Behavior**:
- Slug follows pattern: `title.lower().replace(' ', '-')`

### 10. Default Publishing Status 📝

**Test**: `test_create_blog_published_by_default`

**Scenario**: Blogs are created as published by default.

**Expected Behavior**:
- `is_published = True`
- `published_at` timestamp set

## Test Fixtures

### `app`
- Creates test Flask application with in-memory SQLite database
- Uses testing configuration
- Handles database setup/teardown

### `client`
- Test client for making HTTP requests
- No authentication by default

### `authenticated_client`
- Test client with user authentication
- Uses session-based authentication

### `test_user`
- Creates a test user in the database
- Used for authentication in tests

### `sample_blog_data`
- Sample valid blog data for testing
- Includes title, description, and content

### `existing_blog`
- Creates an existing blog for duplicate testing
- Used in duplicate title test cases

## Coverage Reports

After running tests, coverage reports are generated in:
- **Terminal**: Shows missing lines
- **HTML**: `htmlcov/index.html` - Interactive coverage report

## Test Configuration

### Environment Variables
- `FLASK_ENV=testing`
- `TESTING=True`
- `WTF_CSRF_ENABLED=False` (for testing)

### Database
- Uses in-memory SQLite database
- Fresh database for each test
- Automatic cleanup after tests

## Best Practices

1. **Isolation**: Each test is independent
2. **Fixtures**: Reusable test data and setup
3. **Assertions**: Clear, specific assertions
4. **Coverage**: Aim for high test coverage
5. **Documentation**: Well-documented test cases

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **Database Errors**: Check that test database is properly configured
3. **Authentication Issues**: Verify test user fixtures are working
4. **CSRF Errors**: Ensure CSRF is disabled in test configuration

### Debug Mode

Run tests with verbose output:
```bash
python -m pytest tests/ -v -s
```

## Future Enhancements

1. **Integration Tests**: Test full user workflows
2. **Performance Tests**: Test with large datasets
3. **API Tests**: Test JSON API endpoints
4. **UI Tests**: Test frontend interactions
5. **Load Tests**: Test under concurrent load
