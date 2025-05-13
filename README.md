# AlphaVox

AlphaVox is an advanced AI-powered multimodal communication platform that enables intelligent, adaptive voice and interaction technologies with comprehensive learning journey tracking and mobile-first design.

## Features

- Multi-modal communication support (voice, text, gestures, symbols)
- Self-learning AI architecture with Neural Learning Core (NLC)
- Adaptive conversation complexity based on user profile
- Real-time eye tracking and behavioral analysis
- Comprehensive learning journey tracking
- Caregiver dashboard for monitoring progress
- Responsive, mobile-first design

## Technologies

- Python 3.11 backend with Flask
- PostgreSQL database
- Advanced machine learning (NumPy, scikit-learn)
- Self-modifying code engine
- Dynamic AI learning journey management
- OpenAI and Anthropic API integration

## Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL
- Node.js (for frontend build tools)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/alphavox.git
   cd alphavox
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set up environment variables:
   ```bash
   export DATABASE_URL=postgresql://username:password@localhost:5432/alphavoxdb
   export SESSION_SECRET=your_session_secret
   export OPENAI_API_KEY=your_openai_key
   export ANTHROPIC_API_KEY=your_anthropic_key
   ```

4. Create the database:
   ```bash
   python scripts/db_migrate.py --create-only
   ```

5. Run the application:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   ```

6. Access the application at http://localhost:5000

## AWS Deployment

For detailed AWS deployment instructions, see [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md).

### Quick Deployment Steps

1. Configure AWS credentials:
   ```bash
   aws configure
   ```

2. Initialize Elastic Beanstalk:
   ```bash
   eb init
   ```

3. Create the environment:
   ```bash
   eb create alphavox-production
   ```

4. Deploy:
   ```bash
   eb deploy
   ```

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t alphavox .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 --env-file .env alphavox
   ```

## Project Structure

- `app.py` - Core application setup
- `main.py` - Entry point
- `models.py` - Database models
- `routes/` - API routes
- `templates/` - UI templates
- `static/` - Static assets
- `models/` - ML models
- `data/` - Application data
- `scripts/` - Utility scripts
- `.ebextensions/` - AWS Elastic Beanstalk configuration
- `Dockerfile` - Docker configuration

## API Endpoints

- `/health` - Health check endpoint
- `/api/speech` - Speech generation API
- `/api/recognition` - Speech recognition API
- `/api/behavior` - Behavior analysis API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.