# Blog_Post_API

## Overview

This Blog Post API enables users to create, read, update, and delete blog posts while managing user authentication and post likes. It is built with FastAPI and includes secure JWT-based authentication to handle user registration and login, alongside CRUD functionality for blog posts and the ability for users to like posts. The API is deployed on Render and can be accessed at [https://api-9leq.onrender.com](https://api-9leq.onrender.com).

## Features

- **User Authentication**: Secure JWT-based authentication system allowing users to register, log in, and perform actions based on authentication.
- **CRUD Operations**: Full Create, Read, Update, and Delete (CRUD) functionality for blog posts.
- **Like Feature**: Users can like posts, helping to track popular content.
- **Deployment**: Hosted on Render for live access and testing.

## Tech Stack

- **Backend Framework**: FastAPI for a high-performance, asynchronous web API.
- **Authentication**: JSON Web Tokens (JWT) for secure user sessions.
- **Database**: PostgreSQL for persistent data storage.
- **Deployment**: Render.com for scalable cloud deployment.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/blog_post_api.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd blog_post_api
    ```
3. **Create a virtual environment**:
    ```bash
    python -m venv env
    ```
4. **Activate the virtual environment**:
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source env/bin/activate
        ```
5. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
6. **Set up the Database**:
    Configure your PostgreSQL database settings in the `.env` file.

7. **Run the server**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

- **Register/Login**: Use the `/auth/register` endpoint to create a user account and `/auth/login` to log in and receive a JWT token.
- **Create Posts**: Create blog posts using the `/posts` endpoint, accessible to authenticated users.
- **View, Update, Delete Posts**: Perform CRUD operations on posts with endpoints `/posts/{post_id}`, ensuring secure access.
- **Like Posts**: Like posts by sending requests to `/posts/{post_id}/like`.

## Deployment

The API is live and can be accessed at: [https://api-9leq.onrender.com](https://api-9leq.onrender.com).

## Contact

For any inquiries, please contact yourname@example.com or open an issue in the repository.
