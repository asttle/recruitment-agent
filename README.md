# Recruitment Agent

A Python-based recruitment agent application designed to streamline the hiring process. This application helps automate candidate screening, resume parsing, and interview scheduling using AI.

## Features

- Resume parsing and analysis with AI
- Automated candidate sourcing from external platforms (LinkedIn, CV Library, Naukri)
- Intelligent candidate-job matching using LLM
- Automated email communication for interviews
- Candidate pipeline management and tracking

## Workflow

The Recruitment Agent follows a comprehensive workflow:

1. **Candidate Acquisition**:
   - Process resumes from directly applied candidates
   - Pull potential candidates from external sources (LinkedIn, CV Library, Naukri)

2. **AI-Powered Screening**:
   - Analyze resumes using LLM to extract skills, experience, and qualifications
   - Match candidates to job descriptions based on extracted information
   - Filter candidates using AI-determined match scores

3. **Interview Management**:
   - Automatically send interview invitations to qualified candidates
   - Track candidate responses
   - Schedule interviews for interested candidates
   - Send follow-up communications

## Technology Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **AI/ML**: OpenAI GPT models for resume parsing and candidate matching
- **Infrastructure**: Kubernetes, Docker
- **CI/CD**: GitHub Actions
- **Email**: SMTP integration with email template system

## Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- kubectl and a local Kubernetes cluster (Minikube, k3s, or similar)
- Git
- OpenAI API key (for LLM features)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/recruitment-agent.git
   cd recruitment-agent
   ```

2. Create a `.env` file with your configuration (see `.env.example` for reference)

3. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Run the application locally:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Alternatively, use Docker Compose for local development (includes PostgreSQL and MailHog):
   ```bash
   docker-compose up
   ```

### Running Tests

```bash
pytest
```

### Deployment

#### Deploying to Local Kubernetes Cluster

1. Ensure your Kubernetes cluster is running:
   ```bash
   kubectl cluster-info
   ```

2. Deploy the application:
   ```bash
   cd infra/scripts
   ./deploy.sh dev  # for development environment
   ./deploy.sh prod # for production environment
   ```

3. Verify the deployment:
   ```bash
   kubectl get pods -n recruitment-agent
   ```

## API Endpoints

- `POST /api/candidates/`: Upload candidate resume and information
- `GET /api/candidates/`: List candidates with optional filters
- `POST /api/jobs/`: Create job postings
- `POST /api/search/external/`: Search for candidates from external sources
- `POST /api/candidates/{candidate_id}/contact`: Send interview invitation
- `POST /api/candidates/{candidate_id}/schedule`: Schedule candidate interview

## Project Structure

- `app/`: Application code
  - `api/`: API endpoints and schemas
  - `models/`: Database models
  - `services/`: Business logic including resume parsing and LLM services
  - `core/`: Core application configurations
- `infra/`: Infrastructure as code
  - `k8s/`: Kubernetes manifests with base/overlays pattern
  - `scripts/`: Deployment scripts
- `tests/`: Test suite

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
