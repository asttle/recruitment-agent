# Recruitment Agent

A Python-based recruitment agent application designed to streamline the hiring process. This application helps automate candidate screening, resume parsing, and interview scheduling.

## Features

- Resume parsing and analysis
- Candidate skill matching
- Automated interview scheduling
- Recruitment pipeline management
- Reporting and analytics

## Technology Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Infrastructure**: Kubernetes, Docker
- **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- kubectl and a local Kubernetes cluster (Minikube, k3s, or similar)
- Git

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/recruitment-agent.git
   cd recruitment-agent
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application locally:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Alternatively, use Docker Compose for local development:
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
   ./deploy.sh dev
   ```

3. Verify the deployment:
   ```bash
   kubectl get pods -n recruitment-agent
   ```

## Project Structure

- `app/`: Application code
- `infra/`: Infrastructure as code (Kubernetes manifests)
- `tests/`: Test suite
- `docs/`: Documentation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
