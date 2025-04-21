# AI Property Consultant

## Overview
AI Property Consultant is an intelligent chatbot system designed to provide real estate consultation services in both Thai and English languages. The system uses advanced natural language processing to understand user queries and provide relevant property information with adjustable conversation styles.

## Features
- Bilingual support (Thai/English)
- Multiple consultation styles (Formal, Casual, Friendly, Professional)
- Property search and recommendation
- User authentication and session management
- Chat history tracking
- Property data management via file upload
- MongoDB integration for data persistence
- Vector-based semantic search
- Empathetic response generation

## Tech Stack
- Frontend: React + TypeScript + Vite
- Backend: FastAPI + Python
- Database: MongoDB
- UI Framework: Tailwind CSS
- State Management: React Context
- API Integration: Axios

## System Requirements
- Node.js 16+
- Python 3.8+
- MongoDB 4.4+
- npm or yarn package manager

## Installation

### Backend Setup
1. Navigate to the backend directory:
```bash
cd src/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix
venv\Scripts\activate     # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MongoDB:
- Create a `.env` file in the backend directory
- Add MongoDB connection string:
```
MONGODB_URL=mongodb://localhost:27017/AI
MONGODB_DB=AI
```

### Frontend Setup
1. Install dependencies:
```bash
npm install
# or
yarn install
```

2. Configure environment:
Create `.env` file in the root directory:
```
VITE_API_URL=http://localhost:8000
```

## Running the Application

### Start Backend Server
```bash
cd src/backend
uvicorn main:app --reload
```

### Start Frontend Development Server
```bash
npm run dev
# or
yarn dev
```

## API Endpoints

### Chat API
- POST `/api/chat`
  - Process user queries and return property recommendations
  - Supports conversation style and language selection

### User Management
- POST `/api/register`
  - User registration
- POST `/api/login`
  - User authentication

### Data Management
- POST `/api/upload`
  - Upload property data via CSV/Excel
- GET `/api/styles`
  - Get available consultation styles

### Chat History
- POST `/api/save_history`
  - Save chat history
- GET `/api/chat` (with get_history=true)
  - Retrieve chat history

## Project Structure
```
.
├── src/
│   ├── backend/
│   │   ├── main.py              # FastAPI application
│   │   ├── mongodb_manager.py   # Database operations
│   │   ├── language_models.py   # Response generation
│   │   ├── vector_store.py      # Semantic search
│   │   ├── config.py           # Configuration
│   │   └── requirements.txt    # Python dependencies
│   ├── frontend/
│   │   ├── api.ts             # API integration
│   │   └── components/        # React components
│   └── types/                 # TypeScript types
├── package.json
└── README.md
```

## Key Components

### Backend Components
1. FastAPI Application (`main.py`)
   - API endpoints and request handling
   - Chat processing and response generation
   - File upload handling

2. MongoDB Manager (`mongodb_manager.py`)
   - Database operations
   - Session management
   - User data handling

3. Language Models (`language_models.py`)
   - Response generation
   - Multi-language support
   - Consultation style management

4. Vector Store (`vector_store.py`)
   - Semantic search implementation
   - Property matching

### Frontend Components
1. API Integration (`api.ts`)
   - Backend communication
   - Request/response handling

2. React Components
   - Chat interface
   - Property display
   - User management
   - File upload

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License.

## Support
For support, please open an issue in the repository or contact the development team.
