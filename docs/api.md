# API Documentation

## Authentication

### Login
```http
POST /api/auth/login
```

Request body:
```json
{
  "email": "string",
  "password": "string"
}
```

Response:
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  }
}
```

### Register
```http
POST /api/auth/register
```

Request body:
```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```

Response:
```json
{
  "id": "string",
  "email": "string",
  "name": "string"
}
```

## Properties

### Get Properties
```http
GET /api/properties
```

Query parameters:
- `page`: number (default: 1)
- `limit`: number (default: 10)
- `type`: string (optional)
- `price_min`: number (optional)
- `price_max`: number (optional)
- `location`: string (optional)

Response:
```json
{
  "data": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "price": number,
      "type": "string",
      "location": "string",
      "images": ["string"],
      "features": ["string"]
    }
  ],
  "total": number,
  "page": number,
  "limit": number
}
```

### Get Property Details
```http
GET /api/properties/{id}
```

Response:
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "price": number,
  "type": "string",
  "location": "string",
  "images": ["string"],
  "features": ["string"],
  "details": {
    "bedrooms": number,
    "bathrooms": number,
    "area": number,
    "year_built": number
  }
}
```

## Chat

### Start Chat
```http
POST /api/chat/start
```

Request body:
```json
{
  "property_id": "string",
  "message": "string"
}
```

Response:
```json
{
  "chat_id": "string",
  "message": "string",
  "timestamp": "string"
}
```

### Send Message
```http
POST /api/chat/{chat_id}/message
```

Request body:
```json
{
  "message": "string"
}
```

Response:
```json
{
  "message": "string",
  "timestamp": "string"
}
```

### Get Chat History
```http
GET /api/chat/{chat_id}/history
```

Response:
```json
{
  "messages": [
    {
      "id": "string",
      "content": "string",
      "sender": "user" | "assistant",
      "timestamp": "string"
    }
  ]
}
```

## User Profile

### Get User Profile
```http
GET /api/users/profile
```

Response:
```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "preferences": {
    "property_types": ["string"],
    "locations": ["string"],
    "price_range": {
      "min": number,
      "max": number
    }
  }
}
```

### Update User Profile
```http
PUT /api/users/profile
```

Request body:
```json
{
  "name": "string",
  "preferences": {
    "property_types": ["string"],
    "locations": ["string"],
    "price_range": {
      "min": number,
      "max": number
    }
  }
}
```

Response:
```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "preferences": {
    "property_types": ["string"],
    "locations": ["string"],
    "price_range": {
      "min": number,
      "max": number
    }
  }
}
```

## Error Responses

All API endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "string",
  "message": "string"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Access denied"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "Something went wrong"
}
``` 