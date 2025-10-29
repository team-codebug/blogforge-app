# BlogForge Documentation

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Project Overview

**BlogForge** is a modern, AI-powered blog platform built with Flask that enables users to create, manage, and share blog content with advanced features like AI content generation, social media repurposing, and real-time collaboration. The platform combines the simplicity of traditional blogging with cutting-edge AI capabilities to enhance content creation and distribution.

### Core Philosophy
BlogForge is designed with the modern content creator in mind, providing:
- **Simplicity**: Intuitive interface for content creation
- **Intelligence**: AI-powered content enhancement and repurposing
- **Efficiency**: Automated workflows and real-time collaboration
- **Scalability**: Built to handle multiple users and growing content libraries

---

## Key Features

### 📝 **Content Management**
- **Rich Markdown Editor**: Live preview with syntax highlighting
- **Auto-save**: Automatic saving every 15 seconds during editing
- **Draft System**: Save and manage unpublished content
- **Version Control**: Track changes and revisions
- **Tag Management**: Organize content with customizable tags

### 🤖 **AI Integration**
- **Content Generation**: AI-powered blog descriptions and summaries
- **Social Media Repurposing**: 
  - Convert blogs to LinkedIn posts
  - Generate Twitter thread content
- **Smart Suggestions**: AI-driven content recommendations
- **Multi-Provider Support**: Google Gemini and OpenAI integration

### 🔍 **Discovery & Search**
- **Global Search**: Find content by title, description, or tags
- **User Feed**: Discover content from all authors
- **Filtering**: Advanced filtering by tags, authors, and dates
- **Real-time Search**: Instant search results as you type

### 👥 **User Management**
- **Multi-user Support**: Multiple authors on the same platform
- **User Profiles**: Personalized author pages
- **Authentication**: Secure Google OAuth integration
- **Role-based Access**: User-specific content management

### 📱 **User Experience**
- **Responsive Design**: Works seamlessly on all devices
- **Dark/Light Mode**: User preference support
- **Real-time Updates**: Live content updates
- **Intuitive Navigation**: Clean, modern interface

### 🔒 **Security & Performance**
- **CSRF Protection**: Secure form handling
- **Rate Limiting**: API protection against abuse
- **Input Validation**: Comprehensive data sanitization
- **Session Management**: Secure user sessions

---

## Tech Stack

### **Backend Framework**
- **Flask 3.0.3**: Lightweight Python web framework
- **Python 3.8+**: Modern Python with type hints support

### **Database & ORM**
- **SQLAlchemy 3.1.1**: Powerful ORM for database operations
- **Flask-Migrate 4.0.7**: Database migration management
- **SQLite**: Default database (easily configurable for PostgreSQL/MySQL)

### **Authentication & Security**
- **Flask-Login 0.6.3**: User session management
- **Flask-WTF 1.2.1**: Form handling and CSRF protection
- **Authlib 1.3.1**: OAuth integration (Google)
- **Flask-Limiter 3.8.0**: Rate limiting and API protection

### **AI & Content Processing**
- **Google Gemini API**: Primary AI content generation
- **OpenAI API**: Alternative AI provider support
- **markdown-it-py 3.0.0**: Markdown to HTML conversion
- **Custom AI Services**: Specialized content repurposing

### **Frontend & Styling**
- **TailwindCSS**: Utility-first CSS framework
- **Jinja2 3.1.4**: Template engine
- **Vanilla JavaScript**: Lightweight client-side functionality
- **Responsive Design**: Mobile-first approach

### **Development & Testing**
- **pytest 7.4.3**: Testing framework
- **pytest-flask 1.3.0**: Flask-specific testing utilities
- **pytest-cov 4.1.0**: Code coverage reporting
- **Flask Debug Toolbar**: Development debugging

### **Deployment & Infrastructure**
- **WSGI**: Web Server Gateway Interface
- **Environment Configuration**: Flexible deployment options
- **Database Migrations**: Version-controlled schema changes

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8 or higher**
- **pip3** (Python package manager)
- **Git** (for version control)

### Quick Setup (Recommended)

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd BlogForge
   ```

2. **Run the Automated Setup**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
   
   This script will:
   - Create a Python virtual environment
   - Install all required dependencies
   - Initialize the database with migrations
   - Set up the project structure

3. **Configure Environment Variables**
   
   Edit the `.flaskenv` file:
   ```env
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   SECRET_KEY=your-secure-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

4. **Start the Application**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

5. **Access the Application**
   Open your browser and navigate to `http://localhost:5000`

### Manual Setup

If you prefer manual setup or need to customize the installation:

1. **Create Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Configure Environment**
   Create a `.flaskenv` file with your configuration:
   ```env
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

5. **Start the Application**
   ```bash
   flask run
   ```

### API Key Configuration

#### Google Gemini API
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Add it to your `.flaskenv` file:
   ```env
   GEMINI_API_KEY=your-api-key-here
   ```

#### Optional: OpenAI API
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Add it to your `.flaskenv` file:
   ```env
   OPENAI_API_KEY=your-api-key-here
   AI_PROVIDER=openai
   ```

### Database Configuration

The application uses SQLite by default. To use a different database:

1. **Update Database URL**
   ```env
   DATABASE_URL=postgresql://user:password@localhost/blogforge
   # or
   DATABASE_URL=mysql://user:password@localhost/blogforge
   ```

2. **Apply Migrations**
   ```bash
   flask db upgrade
   ```

---

## Project Structure

```
BlogForge/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app initialization
│   ├── config.py                # Configuration settings
│   ├── models.py                # Database models
│   ├── extensions.py            # Flask extensions
│   ├── ai/                      # AI-related functionality
│   │   ├── __init__.py
│   │   ├── routes.py            # AI API endpoints
│   │   └── services.py          # AI service layer
│   ├── auth/                    # Authentication
│   │   ├── __init__.py
│   │   └── routes.py            # Auth endpoints
│   ├── main/                    # Main application routes
│   │   ├── __init__.py
│   │   └── routes.py            # Dashboard, profile, etc.
│   ├── posts/                   # Blog post management
│   │   ├── __init__.py
│   │   └── routes.py            # CRUD operations
│   ├── templates/               # HTML templates
│   │   ├── layout.html          # Base template
│   │   ├── main/                # Main pages
│   │   └── posts/               # Post-related pages
│   └── static/                  # Static assets
│       ├── css/                 # Stylesheets
│       └── js/                  # JavaScript files
├── migrations/                  # Database migrations
├── tests/                       # Test suite
│   ├── conftest.py             # Test configuration
│   ├── test_posts_routes.py    # Unit tests
│   └── test_blog_workflow_integration.py  # Integration tests
├── instance/                    # Instance-specific files
├── start.sh                     # Setup script
├── run.sh                       # Run script
├── run_tests.sh                 # Test runner
├── requirements.txt             # Python dependencies
├── pytest.ini                  # Test configuration
├── wsgi.py                      # WSGI entry point
└── README.md                    # Project documentation
```

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_APP` | Flask application entry point | `wsgi.py` | Yes |
| `FLASK_ENV` | Environment mode | `development` | No |
| `SECRET_KEY` | Flask secret key | `dev-secret-change-me` | Yes |
| `DATABASE_URL` | Database connection string | SQLite path | No |
| `GEMINI_API_KEY` | Google Gemini API key | None | Yes |
| `OPENAI_API_KEY` | OpenAI API key | None | No |
| `AI_PROVIDER` | AI provider preference | `openai` | No |
| `RATELIMIT_DEFAULT` | Rate limiting | `1000/day` | No |

### Configuration Classes

The application supports multiple configuration environments:

- **DevelopmentConfig**: Debug mode enabled, detailed error pages
- **TestingConfig**: In-memory database, CSRF disabled
- **ProductionConfig**: Secure cookies, optimized settings

---

## API Documentation

### Authentication Endpoints

#### `POST /auth/google`
Initiates Google OAuth authentication flow.

#### `GET /auth/google/callback`
Handles Google OAuth callback and creates user session.

### Blog Management Endpoints

#### `GET /posts/`
Retrieves list of user's blog posts.

**Query Parameters:**
- `filter`: `published` or `drafts` (optional)

#### `POST /posts/`
Creates a new blog post.

**Request Body:**
```json
{
  "title": "Blog Post Title",
  "description": "Blog description",
  "content": "Markdown content"
}
```

#### `GET /posts/<int:blog_id>`
Retrieves a specific blog post.

#### `PUT /posts/<int:blog_id>`
Updates an existing blog post.

#### `DELETE /posts/<int:blog_id>`
Deletes a blog post.

### AI Endpoints

#### `POST /api/ai/generate-description`
Generates blog description using AI.

**Request Body:**
```json
{
  "title": "Blog title",
  "content": "Blog content"
}
```

#### `POST /api/ai/blog-to-linkedin`
Converts blog to LinkedIn post format.

#### `POST /api/ai/blog-to-twitter-thread`
Converts blog to Twitter thread format.

### Utility Endpoints

#### `GET /posts/render-markdown`
Renders markdown to HTML.

**Query Parameters:**
- `text`: Markdown text to render

---

## Testing

### Running Tests

#### Run All Tests
```bash
./run_tests.sh
```

#### Run Specific Test Suites
```bash
# Unit tests only
pytest tests/test_posts_routes.py -v

# Integration tests only
pytest tests/test_blog_workflow_integration.py -v

# With coverage report
pytest --cov=app --cov-report=html
```

### Test Structure

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test complete user workflows
- **Fixtures**: Reusable test data and setup
- **Coverage**: Comprehensive code coverage reporting

### Test Coverage

Current test coverage includes:
- ✅ Blog creation and management
- ✅ User authentication flows
- ✅ AI content generation
- ✅ Search functionality
- ✅ Error handling scenarios

---

## Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=your-production-database-url
   ```

2. **Database Migration**
   ```bash
   flask db upgrade
   ```

3. **WSGI Server**
   ```bash
   gunicorn wsgi:app
   ```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "wsgi:app"]
```

### Environment-Specific Configuration

- **Development**: Debug mode, detailed errors
- **Testing**: In-memory database, test-specific settings
- **Production**: Secure settings, optimized performance

---

## Troubleshooting

### Common Issues

#### 1. Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf .venv
./start.sh
```

#### 2. Database Errors
```bash
# Reset database
rm instance/app.db
flask db upgrade
```

#### 3. Missing Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. API Key Errors
- Verify API keys in `.flaskenv`
- Check API key validity
- Ensure proper environment variable loading

#### 5. Permission Issues
```bash
# Fix script permissions
chmod +x start.sh run.sh run_tests.sh
```

### Debug Mode

Enable debug mode for detailed error information:
```env
FLASK_ENV=development
DEBUG=True
```

### Logs

Check application logs for detailed error information:
- Console output during development
- Server logs in production
- Database query logs (if enabled)

---

## Contributing

### Development Workflow

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Changes**
4. **Run Tests**
   ```bash
   ./run_tests.sh
   ```
5. **Commit Changes**
   ```bash
   git commit -m "Add your feature"
   ```
6. **Push and Create Pull Request**

### Code Standards

- Follow PEP 8 Python style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages

### Testing Requirements

- All new features must include tests
- Maintain or improve test coverage
- Integration tests for user workflows
- Unit tests for individual functions

---

## Support

For technical support and questions:

1. **Check Documentation**: Review this document and README
2. **Search Issues**: Look for existing solutions
3. **Create Issue**: Provide detailed problem description
4. **Community**: Engage with the development community

---

**Happy Blogging with BlogForge! 🚀**

*This documentation is maintained alongside the codebase. For the most up-to-date information, always refer to the latest version.*
