# Recruitment Agent Frontend

A modern, responsive frontend for the Recruitment Agent application built with React, Vite, and Tailwind CSS.

## Features

- Dashboard with recruitment metrics and candidate overview
- Candidate management with filtering and search
- Job posting management
- External candidate search integration
- Interview scheduling
- Modern UI with responsive design

## Technology Stack

- **React** - UI Library
- **Vite** - Build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Routing
- **React Query** - Data fetching and caching
- **React Icons** - Icon components
- **React Hook Form** - Form handling

## Getting Started

### Prerequisites

- Node.js 14+ and npm

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Project Structure

```
frontend/
├── src/
│   ├── assets/       # Static assets like images
│   ├── components/   # Reusable components
│   │   ├── ui/       # UI components like buttons, inputs, etc.
│   │   └── layout/   # Layout components
│   ├── hooks/        # Custom React hooks
│   ├── pages/        # Page components
│   ├── services/     # API services
│   ├── styles/       # Global styles
│   ├── utils/        # Utility functions
│   ├── App.jsx       # Main App component with routing
│   └── main.jsx      # Entry point
├── index.html        # HTML template
├── vite.config.js    # Vite configuration
└── tailwind.config.js # Tailwind CSS configuration
```

## API Integration

This frontend connects to the Recruitment Agent backend API by default at `http://localhost:8000`. You can change this configuration in the Vite proxy settings if needed.

## Deployment

To deploy the frontend, first build the project:

```bash
npm run build
```

This will create a `dist` folder that can be served by any static file server. 