# สถาปัตยกรรมระบบ AI Property Consultant

## ภาพรวมระบบ

ระบบ AI Property Consultant ถูกออกแบบด้วยสถาปัตยกรรมแบบ Microservices ที่ประกอบด้วยส่วนหลักๆ ดังนี้:

### 1. Frontend (React + TypeScript)
- ใช้ Next.js เป็น framework หลัก
- ใช้ Tailwind CSS สำหรับ styling
- ใช้ Zustand สำหรับ state management
- ใช้ React Query สำหรับ data fetching

### 2. Backend (FastAPI + Python)
- RESTful API สำหรับจัดการข้อมูล
- WebSocket สำหรับการแชทแบบ real-time
- Vector Database สำหรับการค้นหาอสังหาริมทรัพย์
- Authentication และ Authorization

### 3. ฐานข้อมูล
- MongoDB สำหรับเก็บข้อมูลผู้ใช้และประวัติการแชท
- Vector Database สำหรับเก็บ embeddings ของอสังหาริมทรัพย์

### 4. AI Components
- LLM Integration สำหรับการตอบคำถาม
- Vector Search สำหรับการค้นหาอสังหาริมทรัพย์
- User Analysis สำหรับวิเคราะห์ความสนใจของผู้ใช้

## โครงสร้างไฟล์

```
.
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Next.js pages
│   │   ├── services/      # API services
│   │   ├── store/         # Zustand store
│   │   └── types/         # TypeScript types
│   └── public/            # Static files
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── models/       # Data models
│   │   └── services/     # Business logic
│   └── tests/            # Test files
└── docs/                 # Documentation
```

## การสื่อสารระหว่าง Components

1. **Frontend-Backend Communication**
   - REST API สำหรับการจัดการข้อมูลทั่วไป
   - WebSocket สำหรับการแชทแบบ real-time
   - GraphQL สำหรับการ query ข้อมูลที่ซับซ้อน

2. **Backend-Database Communication**
   - MongoDB Driver สำหรับการจัดการข้อมูล
   - Vector Database API สำหรับการค้นหา embeddings

3. **AI Integration**
   - API calls ไปยัง LLM service
   - Vector search สำหรับการค้นหาอสังหาริมทรัพย์
   - User analysis สำหรับการวิเคราะห์ความสนใจ

## Security

1. **Authentication**
   - JWT-based authentication
   - OAuth 2.0 สำหรับ social login
   - Session management

2. **Authorization**
   - Role-based access control
   - Permission management
   - API key management

3. **Data Protection**
   - Encryption at rest
   - Secure communication (HTTPS)
   - Input validation

## Scalability

1. **Horizontal Scaling**
   - Load balancing
   - Database sharding
   - Caching strategy

2. **Performance Optimization**
   - CDN integration
   - Database indexing
   - Query optimization

## Monitoring and Logging

1. **System Monitoring**
   - Health checks
   - Performance metrics
   - Error tracking

2. **Logging**
   - Application logs
   - Access logs
   - Error logs

## Deployment

1. **Development**
   - Docker containers
   - Local development environment
   - CI/CD pipeline

2. **Production**
   - Kubernetes orchestration
   - Auto-scaling
   - Backup and recovery 