# PharmaTrack - Advanced Drug Safety Intelligence Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pharmatrack-system.streamlit.app/)
![GitHub last commit](https://img.shields.io/github/last-commit/makrame5/PharmaTrack---Drug-Safety-Monitoring-System?style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)



## Overview

PharmaTrack is an advanced drug safety intelligence platform designed to transform how healthcare professionals monitor and prevent Adverse Drug Events (ADEs). By leveraging real-world data and predictive analytics, we aim to enhance patient safety and improve clinical decision-making.

## Project Objectives
### Primary Goals
- Build an end-to-end data pipeline for hospital ADE data management
- Develop predictive models to identify high-risk patients
- Create interactive dashboards for real-time monitoring
- Establish data quality and governance protocols

###  Key Features
- **Data Ingestion**: Seamless integration with hospital systems and FDA databases
- **Risk Prediction**: Machine learning models to forecast ADE probabilities
- **Interactive Dashboard**: Real-time visualization of key metrics
- **Alert System**: Proactive notifications for high-risk cases
- **Standardized Reporting**: Compliance with healthcare data standards


## Technical Architecture
### 📊 Tech Stack
- **Backend**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Database**: MongoDB (NoSQL)
- **Dashboard**: Streamlit

### 🏗️ System Components
1. **Data Ingestion Layer**
   - API integrations (FDA OpenFDA, hospital systems)


2. **Data Lake**
   - Raw data storage (CSV, JSON)
   - Data validation and quality checks

3. **Data Processing**
   - ETL pipelines
   - Feature engineering
   - Data standardization

4. **Visualization**
   - Interactive dashboards
   - Real-time monitoring
   - Custom reporting



##  Key Metrics Tracked
- ADE incidents by department/hospital/month
- Patient risk profiles
- Medication interaction alerts
- Quality indicators
- Performance metrics


## Getting Started
### Prerequisites
- Python 3.8+
- MongoDB instance
- PostgreSQL (optional)
- API keys for data sources

### Installation
```bash
# Clone the repository
git clone https://github.com/makrame5/PharmaTrack---Drug-Safety-Monitoring-System.git
cd PharmaTrack---Drug-Safety-Monitoring-System

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Running the Application
```bash
# Start the Streamlit dashboard
streamlit run app.py

# For production (using Gunicorn)
gunicorn app:app
```

## Contributing

Contributions are always welcome!




## Contact
For inquiries or support, please [open an issue](https://github.com/makrame5/PharmaTrack---Drug-Safety-Monitoring-System/issues) 

or Contact
https://himedi-makrame.vercel.app/


## Key Improvements


Made with ❤️ by HIMEDI Makrame [![GitHub](https://img.icons8.com/ios-filled/20/000000/github.png)](https://github.com/makrame5)


