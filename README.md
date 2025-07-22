# 📚 BookStore Web App

A full-featured web application built with **Django** for managing an online bookstore. This platform allows users to browse, search, and manage books, offering a complete e-commerce experience with an integrated blog.

## 📖 About the Project

This project serves as a comprehensive demonstration of my skills in **Python** and **Django** web development. It encompasses key aspects of a modern web application, including:

* **User Authentication & Authorization:** Secure user registration, login, and logout functionalities.
* **Product Catalog Management:** Robust CRUD (Create, Read, Update, Delete) operations for books.
* **Shopping Cart Functionality:** Seamless addition and removal of items, with dynamic updates.
* **Order Processing:** A streamlined checkout flow to finalize purchases.
* **Blogging Platform:** An integrated blog where users (or staff) can create, view, and manage posts.
* **RESTful APIs:** Exposed endpoints for products and blog posts, leveraging Django REST Framework.
* **Database Management:** Utilizes **PostgreSQL** for efficient and reliable data storage.

The application is designed to be intuitive and provides a solid foundation for an e-commerce platform.

## ✨ Key Features

* **E-commerce Core:**
    * **Book Listing:** Display all available books with essential details.
    * **Shopping Cart:** Add, remove, and update quantities of books in the cart.
    * **Checkout Process:** A multi-step checkout with order finalization.
    * **Product Management (Admin/Staff only):** Secure interface for adding, editing, and deleting books.
    * **Dynamic Cart:** Cart items update in real-time.
* **User Management:**
    * Secure user **registration** and **login/logout** system.
    * User profiles to view and update personal information.
* **Integrated Blog:**
    * View a list of **blog posts**.
    * Detailed view for each blog post.
    * **Create, update, and delete** blog posts (authentication required, and author-specific deletion).
* **API Endpoints:**
    * RESTful API for **Products** (`/api/products/`) supporting GET and POST requests.
    * RESTful API for **Blog Posts** (`/api/blogposts/`) supporting GET requests.
* **Database:**
    * Uses **PostgreSQL** as the primary database for data persistence.
* **Frontend:**
    * Utilizes **HTML**, **CSS**, and **JavaScript** for a responsive user interface.
    * (Optional: Mention Bootstrap/other CSS frameworks if used for styling.)

## 🚀 Live Demonstration

**(If you have deployed the project to a live server, provide the URL here. For Django apps, services like Render.com, PythonAnywhere, or Heroku (though Heroku's free tier has changed) are common.)**

[Link to Live Demo](https://your-live-demo-url.com) (Replace with your actual live demo URL)

## 📸 Screenshots & Demos

**(This is CRUCIAL for web projects. Include high-quality screenshots or animated GIFs that demonstrate the core functionalities. Place these files in a `/docs/assets/` folder in your repository for better organization.)**

<p align="center">
  <img src="docs/assets/homepage.png" alt="BookStore Homepage" width="700"/>
  <br>
  <em>The main store page displaying a selection of books.</em>
</p>
<p align="center">
  <img src="docs/assets/cart-page.png" alt="Shopping Cart Page" width="700"/>
  <br>
  <em>View of the shopping cart with added items.</em>
</p>
<p align="center">
  <img src="docs/assets/blog-list.png" alt="Blog List Page" width="700"/>
  <br>
  <em>The blog section displaying various posts.</em>
</p>
## 💻 Technologies Used

This project is built using a robust stack of web technologies:

**Backend & Core:**
* **Python 3.x:** The primary programming language.
* **Django 4.2.x:** High-level Python web framework.
* **Django REST Framework:** For building powerful Web APIs.

**Frontend:**
* **HTML5:** For structuring the web content.
* **CSS3:** For styling the application.
* **JavaScript:** For interactive elements and dynamic updates (e.g., cart functionality).
* **Bootstrap:** (If used, specify version) A popular CSS framework for responsive design.

**Database:**
* **PostgreSQL:** A powerful open-source relational database system.

**Tools & Other Libraries:**
* **Git & GitHub:** For version control and collaboration.
* **`python-dotenv`:** For managing environment variables securely.
* **`pillow`:** (If images are uploaded) Python Imaging Library.

## ⚙️ Local Installation & Setup

Follow these steps to get the BookStore Web App running on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/EliArn99/BookStore_Web_App.git](https://github.com/EliArn99/BookStore_Web_App.git)
    cd BookStore_Web_App
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    # For Windows:
    .\venv\Scripts\activate
    # For macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Project Dependencies:**
    All necessary Python libraries are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup (PostgreSQL):**
    * Ensure you have a **PostgreSQL** server installed and running on your system.
    * Create a new database for this project (e.g., `bookstore_db`).
    * **Environment Variables (`.env` file):**
        Create a file named `.env` in the root directory of your project (where `manage.py` is located). Add the following variables, replacing the placeholder values with your actual database credentials and a strong secret key:
        ```env
        SECRET_KEY='your_very_secret_key_here_for_production_use_a_strong_one'
        DEBUG=True
        DB_NAME='bookstore_db'
        DB_USER='your_db_username'
        DB_PASSWORD='your_db_password'
        DB_HOST='localhost' # Or your PostgreSQL host if not local
        DB_PORT='5432'
        ALLOWED_HOSTS='localhost,127.0.0.1' # Add other domains if deploying
        ```
    * Your `settings.py` already includes `env()` calls for these, ensuring secure handling of sensitive data.

5.  **Run Database Migrations:**
    Apply the database schema changes based on your models.
    ```bash
    python manage.py makemigrations books
    python manage.py migrate
    ```

6.  **Create a Superuser (Optional but Recommended):**
    This allows you to access the Django Admin panel to manage books, users, and blog posts.
    ```bash
    python manage.py createsuperuser
    ```

7.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```
    The application should now be accessible in your web browser at: `http://127.0.0.1:8000/`.

## 🧪 Running Tests

To run the project's unit and integration tests (which you've written in `tests.py`), use the following command:
```bash
python manage.py test
