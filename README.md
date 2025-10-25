# BlogForge

A modern blog platform built with Flask, featuring AI-powered content generation, social media repurposing, and a beautiful user interface.

## Features

- 📝 **Rich Blog Editor**: Markdown support with live preview
- 🤖 **AI Integration**: Powered by Google Gemini for content generation
- 🔄 **Social Media Repurposing**: Convert blogs to LinkedIn posts and Twitter threads
- 🏷️ **Tag System**: Organize content with customizable tags
- 🔍 **Search Functionality**: Find blogs by title, description, or tags
- 📱 **Responsive Design**: Beautiful UI that works on all devices
- 💾 **Auto-save**: Automatic saving while editing
- 📊 **Draft System**: Save and manage draft posts
- 👥 **Multi-user**: Support for multiple authors

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip3

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BlogForge
   ```

2. **Run the setup script**
   ```bash
   ./start.sh
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Initialize the database
   - Set up the project structure

3. **Configure your environment**
   Edit `.flaskenv` and update:
   - `SECRET_KEY`: Generate a secure secret key
   - `GEMINI_API_KEY`: Get your API key from [Google AI Studio](https://aistudio.google.com/)

4. **Start the application**
   ```bash
   ./run.sh
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Manual Setup

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Start the application
flask run
```

## Project Structure

```
BlogForge/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models
│   ├── ai/                  # AI-related routes
│   ├── main/                # Main application routes
│   ├── posts/               # Blog post routes
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, and assets
├── migrations/              # Database migrations
├── uploads/                 # File uploads
├── start.sh                 # Setup script
├── run.sh                   # Run script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration

### Environment Variables

Create a `.flaskenv` file with the following variables:

```env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///blogforge.db
GEMINI_API_KEY=your-gemini-api-key-here
```

### Database

The application uses SQLite by default. To use a different database:

1. Update `DATABASE_URL` in `.flaskenv`
2. Run `flask db upgrade` to apply migrations

## API Keys

### Google Gemini API

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Add it to your `.flaskenv` file

## Usage

### Creating a Blog Post

1. Click "New Post" in the sidebar
2. Write your content in Markdown
3. Add tags to categorize your post
4. Click "Save" to publish

### AI Features

When editing a post, you can:
- **Repurpose to LinkedIn**: Convert your blog to a LinkedIn post
- **Generate Tweet Thread**: Create a Twitter thread from your blog
- **Auto-save**: Your changes are automatically saved every 15 seconds

### Search

Use the search bar in the header (Feed page only) to find blogs by:
- Title
- Description
- Tags
- Author

## Development

### Running in Development Mode

```bash
source .venv/bin/activate
flask run --debug
```

### Database Migrations

```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

### Adding New Features

1. Create new routes in the appropriate blueprint
2. Add templates in the `templates/` directory
3. Update the database models if needed
4. Create and apply migrations

## Troubleshooting

### Common Issues

1. **Virtual environment not found**
   ```bash
   ./start.sh
   ```

2. **Database errors**
   ```bash
   flask db upgrade
   ```

3. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **API key errors**
   - Check your `.flaskenv` file
   - Verify your Gemini API key is valid

### Logs

Check the console output for error messages. The application logs important events and errors.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Create an issue in the repository

---

**Happy Blogging! 🚀**
