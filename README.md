# 🚀 Compli AI - Intelligent Compliance Management System

<div align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/Firebase-039BE5?style=for-the-badge&logo=Firebase&logoColor=white" alt="Firebase" />
</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Usage](#usage)
- [Contributors](#contributors)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [License](#license)

## 🔍 Overview

**Compli AI** is an intelligent compliance management system designed to streamline and automate compliance checks for cross-border shipments. The platform leverages machine learning algorithms to analyze shipment data, detect potential compliance issues, and generate comprehensive reports to ensure regulatory adherence.

### 🎯 Problem Statement

International shipping involves complex compliance requirements that vary by country, product type, and shipping method. Manual compliance checks are:
- Time-consuming and error-prone
- Require extensive regulatory knowledge
- Lead to delayed shipments and penalties
- Difficult to scale for large volumes

### ✨ Solution

Compli AI provides an automated solution that:
- Performs real-time compliance validation
- Generates detailed compliance reports
- Identifies required documents and certifications
- Supports multiple input methods (manual entry, file upload)
- Provides HS Code lookup functionality

## 🚀 Features

### Core Features
- **🔍 Compliance Check**: Real-time validation of shipment data against regulatory requirements
- **📊 Dashboard**: Comprehensive overview of compliance status and statistics
- **📄 Report Generation**: Detailed PDF reports with compliance status and recommendations
- **📁 File Upload**: Bulk compliance checking via CSV/Excel file upload
- **✍️ Manual Entry**: Individual shipment compliance verification
- **🔢 HS Code Lookup**: Product-specific Harmonized System code identification

### Advanced Features
- **🤖 AI-Powered Analysis**: Machine learning-based compliance prediction
- **🚫 Banned Product Detection**: Automatic identification of prohibited items
- **🌍 Country-Specific Rules**: Compliance validation based on origin/destination countries
- **💰 Value-Based Requirements**: Document requirements based on declared value thresholds
- **🔐 User Authentication**: Secure login with Firebase integration
- **📱 Responsive Design**: Mobile-friendly interface

## 🛠 Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **Routing**: React Router v7
- **Forms**: Formik + Yup validation
- **State Management**: React Hooks
- **Authentication**: Firebase Auth
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Build Tool**: Vite

### Backend
- **Framework**: Flask (Python)
- **Database**: MongoDB
- **ML Libraries**: scikit-learn, pandas, numpy
- **File Processing**: openpyxl for Excel files
- **CORS**: Flask-CORS
- **Data Processing**: scipy for sparse matrices

### DevOps & Tools
- **Version Control**: Git
- **Package Managers**: npm (frontend), pip (backend)
- **Code Quality**: ESLint, TypeScript
- **Deployment**: Vercel (frontend), local/cloud (backend)

## 🏗 Project Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│   (React)       │◄──►│   (Flask)       │◄──►│   (MongoDB)     │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • ML Models     │    │ • Compliance    │
│ • Forms         │    │ • API Routes    │    │   Reports       │
│ • Reports       │    │ • File Upload   │    │ • HS Codes      │
│ • Auth          │    │ • Validation    │    │ • User Data     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow
1. **Input**: User submits compliance data via forms or file upload
2. **Processing**: Backend validates data using ML models and business rules
3. **Analysis**: System checks against banned products, country restrictions, and value thresholds
4. **Storage**: Results stored in MongoDB with unique identifiers
5. **Output**: Compliance status, detailed reports, and recommendations returned to user

## 📦 Installation

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.8 or higher)
- MongoDB (local or cloud instance)
- Git

### Clone Repository
```bash
git clone https://github.com/vitthal-07/CompliAI.git
cd LogiTHON
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend will be available at `http://localhost:5000`

### Environment Configuration

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000
VITE_FIREBASE_API_KEY=your_firebase_api_key
```

#### Backend (.env)
```env
MONGODB_URI=mongodb://localhost:27017/
FLASK_ENV=development
```

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Single Compliance Check
```http
POST /compliance-check
Content-Type: application/json

{
  "item_name": "Laptop",
  "courier": "DHL",
  "OriginCountry": "India",
  "weight": 2.5,
  "length": 35,
  "breadth": 25,
  "height": 3,
  "declared_value": 50000,
  "hscode": "8471300000",
  "input_text": "Gaming laptop with high-end specifications"
}
```

#### 2. File Upload Compliance Check
```http
POST /compliance-check-file
Content-Type: multipart/form-data

file: [CSV/Excel file with compliance data]
```

#### 3. Get All Reports
```http
GET /compliance-reports
```

#### 4. HS Code Lookup
```http
GET /suggest?product_name=laptop
```

### Response Format
```json
{
  "_id": "unique_report_id",
  "status": "Compliant|Flagged",
  "reasons": ["Array of compliance issues"],
  "required_documents": ["List of required documents"],
  "required_approvals": ["List of required approvals"],
  "required_certifications": ["List of required certifications"],
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## 💻 Usage

### 1. User Registration/Login
- Sign up with email/password or Google OAuth
- Complete profile with company details

### 2. Compliance Check
- **Manual Entry**: Fill out the compliance form with shipment details
- **File Upload**: Upload CSV/Excel file with multiple shipments
- **HS Code Lookup**: Search for product-specific codes

### 3. View Results
- Real-time compliance status (Compliant/Flagged)
- Detailed reasons for non-compliance
- Required documents and certifications
- Downloadable PDF reports

### 4. Dashboard
- Overview of all compliance checks
- Statistics and trends
- Recent activity tracking

## 👥 Contributors

<div align="center">

### 🏆 Core Development Team

</div>

| Contributor | Role | Expertise | GitHub | LinkedIn |
|-------------|------|-----------|---------|----------|
| **🚀 Vitthal Biradar** | **Full Stack Developer & Team Lead** | React, Flask, System Architecture | [@vitthal-07](https://github.com/vitthal-07) | [LinkedIn](https://linkedin.com/in/vitthal-biradar) |
| **💻 Shivanshi Yadav** | **Frontend Developer & UI/UX Designer** | React, TypeScript, Tailwind CSS, User Experience | [@shivanshi](https://github.com/shivanshi) | [LinkedIn](https://linkedin.com/in/shivanshi-yadav) |
| **🔧 Anup Nalwade** | **Backend Developer & ML Engineer** | Python, Machine Learning, Data Processing | [@anup-nalwade](https://github.com/anup-nalwade) | [LinkedIn](https://linkedin.com/in/anup-nalwade) |
| **📊 Swati Yadawar** | **Database Engineer & QA Specialist** | MongoDB, Data Modeling, Testing | [@swati-yadawar](https://github.com/swati-yadawar) | [LinkedIn](https://linkedin.com/in/swati-yadawar) |

### 🎯 Individual Contributions

#### Vitthal Biradar - Team Lead & Full Stack Developer
- **Frontend**: 
  - React application architecture and routing setup
  - TypeScript implementation and type safety
  - Firebase authentication integration
  - Dashboard and analytics components
  - State management and data flow optimization

- **Backend**: 
  - Flask application structure and API design
  - MongoDB integration and data modeling
  - CORS configuration and security implementation
  - File upload functionality for CSV/Excel processing

- **DevOps**: 
  - Project structure and build configuration
  - Version control strategy and Git workflow
  - Deployment pipeline setup

#### Shivanshi Yadav - Frontend Developer & UI/UX Designer
- **UI/UX Design**:
  - Modern, responsive design system with Tailwind CSS
  - Component library integration with shadcn/ui
  - User experience flow and interaction design
  - Accessibility compliance and mobile optimization

- **Frontend Development**:
  - Complex form handling with Formik and validation
  - Interactive compliance check interfaces
  - Real-time data visualization and charts
  - Animation and micro-interactions with Framer Motion

- **User Experience**:
  - Intuitive navigation and user workflows
  - Error handling and user feedback systems
  - Performance optimization and loading states

#### Anup Nalwade - Backend Developer & ML Engineer
- **Machine Learning**:
  - Compliance prediction model development using scikit-learn
  - TF-IDF vectorization for text analysis
  - Model training and validation pipeline
  - Feature engineering for compliance data

- **Backend Logic**:
  - Business rule implementation for compliance checking
  - Banned product and country restriction algorithms
  - Value-based requirement calculation
  - Data processing and validation logic

- **API Development**:
  - RESTful API design and implementation
  - File processing endpoints for bulk operations
  - Error handling and response formatting

#### Swati Yadawar - Database Engineer & QA Specialist
- **Database Design**:
  - MongoDB schema design and optimization
  - Data relationship modeling
  - Index strategy for performance optimization
  - Data migration and seeding scripts

- **Quality Assurance**:
  - End-to-end testing strategy and implementation
  - API testing and validation
  - Cross-browser compatibility testing
  - Performance testing and optimization

- **Data Management**:
  - Compliance data standardization
  - HS Code database integration
  - Backup and recovery procedures
  - Data analytics and reporting support

### 🤝 Team Collaboration

- **Project Management**: Agile development methodology with regular sprints
- **Communication**: Daily standups and weekly progress reviews
- **Code Quality**: Peer code reviews and collaborative problem-solving
- **Documentation**: Comprehensive technical documentation and API specifications

## 📁 Project Structure

```
LogiTHON/
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── ui/           # shadcn/ui components
│   │   │   ├── Header.tsx    # Application header
│   │   │   ├── Sidebar.tsx   # Navigation sidebar
│   │   │   └── Footer.tsx    # Application footer
│   │   ├── pages/            # Page components
│   │   │   ├── HomePage.tsx          # Landing page
│   │   │   ├── Dashboard.tsx         # Main dashboard
│   │   │   ├── LoginInPage.tsx       # User login
│   │   │   ├── SignUpPage.tsx        # User registration
│   │   │   ├── GetHsCode.tsx         # HS code lookup
│   │   │   ├── ComplianceReportPage.tsx  # Reports view
│   │   │   └── ComplianceCheck/      # Compliance checking
│   │   │       ├── ComplianceCheck.tsx
│   │   │       └── compliancePages/
│   │   │           ├── ComplianceCSV.tsx     # File upload
│   │   │           └── ComplianceCheckManual.tsx  # Manual entry
│   │   ├── lib/              # Utility functions
│   │   ├── types.ts          # TypeScript type definitions
│   │   ├── firebase-config.ts # Firebase configuration
│   │   └── main.tsx          # Application entry point
│   ├── public/               # Static assets
│   ├── package.json          # Dependencies and scripts
│   └── tailwind.config.js    # Tailwind CSS configuration
│
├── backend/                   # Flask backend application
│   ├── app.py                # Main Flask application
│   ├── models/               # ML models and vectorizers
│   │   ├── compliance_model.pkl
│   │   └── tfidf_vectorizer.pkl
│   ├── compliance_dataset.xlsx  # Baseline compliance data
│   ├── requirements.txt      # Python dependencies
│   └── README.md            # Backend documentation
│
└── README.md                 # Project documentation
```

## 🎨 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

### Compliance Check
![Compliance Check](https://via.placeholder.com/800x400?text=Compliance+Check+Screenshot)

### Reports
![Reports](https://via.placeholder.com/800x400?text=Reports+Screenshot)

## 🚀 Deployment

### Frontend (Vercel)
```bash
npm run build
vercel --prod
```

### Backend (Heroku/Railway)
```bash
# Using Heroku
heroku create compliai-backend
git push heroku main

# Using Railway
railway login
railway init
railway deploy
```

## 🔄 Development Workflow

1. **Feature Branch**: Create feature branch from `main`
2. **Development**: Implement feature with tests
3. **Code Review**: Submit PR for team review
4. **Testing**: Automated testing and manual QA
5. **Deployment**: Merge to main and deploy

## 📈 Future Enhancements

- [ ] **Real-time Notifications**: WebSocket integration for live updates
- [ ] **Advanced Analytics**: Machine learning insights and predictions
- [ ] **Mobile App**: Native mobile application for iOS/Android
- [ ] **API Integration**: Third-party logistics and customs APIs
- [ ] **Multi-language Support**: Internationalization for global users
- [ ] **Blockchain Integration**: Immutable compliance records
- [ ] **Advanced ML Models**: Deep learning for better accuracy

## 🐛 Known Issues

- File upload limited to 10MB (configurable)
- MongoDB connection timeout in development
- PDF generation requires modern browser

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 📞 Support

For support, email support@compliai.com or join our Slack channel.

## 🙏 Acknowledgments

- **LogiTHON Hackathon** for providing the platform and inspiration
- **Open Source Community** for the amazing tools and libraries
- **MongoDB** for flexible database solutions
- **Firebase** for authentication services
- **Vercel** for seamless deployment

---

<div align="center">
  <p><strong>Made with ❤️ by Team Compli AI</strong></p>
  <p>© 2024 Compli AI. All rights reserved.</p>
</div>
