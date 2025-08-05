<div align="center">
  <h1>Expense Tracker API (Backend) ⚙️</h1>
</div>
<div align="center">

*The backend data processing layer for the Data-Driven Expense Analytics Platform, built with FastAPI.*

![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?style=for-the-badge&logo=mysql)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)

</div>

---

This repository contains the backend API for the **Data-Driven Expense Analytics Platform**. It is built with FastAPI and connects to a MySQL database to handle all data persistence, aggregation, and business logic.

This API serves as the data processing layer for the main application, transforming raw data into analysis-ready formats for the frontend dashboards.

---

## 🚀 Main Project & Live Demo

For a full project description, a live demo, and complete setup instructions, please visit the main frontend repository. It contains the comprehensive README that explains the entire data lifecycle of the project.

<div align="center">
  <strong><a href="https://github.com/Nayan-Reddy/expense-tracker-frontend/tree/main">➡️ View Main Project & Analytics Showcase Here</a></strong>
</div>

---

## 🛠️ API Functionality

* **CRUD Operations:** Handles creating, reading, and deleting user expense records.
* **Data Aggregation:** Provides endpoints that return summarized and pivoted data for analytics.
* **Session Management:** Processes requests based on a unique `session_id` to ensure data privacy.
* **Demo Data Control:** Includes an endpoint to reset the database to its initial demo state.
