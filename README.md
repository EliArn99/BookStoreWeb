# BookStoreWeb

# Django Project: BookWeb Demo

A web application built using Django Framework, featuring user authentication, e-commerce functionalities, role-based access control, and API endpoints.

## Features
- Public and private sections with role-based access control.
- User registration, login, and logout.
- Shopping cart, checkout process, and order management.
- Blog functionality with CRUD operations for authenticated users.
- RESTful APIs for products and blog posts.
- PostgreSQL database integration.
- Admin interface customization for superusers and staff.

---

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL



# 📚 BookStore Web App

Кратко, но ясно описание какво прави приложението и защо е създадено.

## 📖 За проекта

Това е уеб приложение за управление на онлайн книжарница, което позволява на потребителите да се регистрират, да преглеждат наличните книги, да търсят конкретни заглавия и автори, както и да управляват (добавят, редактират, изтриват) книги. Проектът демонстрира умения в бекенд разработката с Django и работа с база данни PostgreSQL, както и основни фронтенд умения.

## ✨ Функционалности

* **Потребителски профили:** Регистрация, вход/изход, потребителски профили.
* **Управление на книги:** CRUD операции (създаване, четене, актуализиране, изтриване) за книги.
* **Търсене и филтриране:** Възможност за търсене на книги по заглавие или автор.
* **Преглед на детайли:** Подробна страница за всяка книга с описание, автор и т.н.
* **Адаптивен дизайн:** (Ако е приложимо) Удобен за употреба на различни устройства.

## 🚀 Демонстрация на живо

[Линк към демото на живо](https://your-live-demo-url.com) (Ако имаш)

## 📸 Скрийншоти

<p align="center">
  <img src="path/to/screenshot1.png" alt="Начална страница" width="400"/>
  <br>
  <em>Начална страница на BookStore Web App</em>
</p>
<p align="center">
  <img src="path/to/screenshot2.png" alt="Страница за книга" width="400"/>
  <br>
  <em>Примерна страница за детайли на книга</em>
</p>
## 💻 Технологии

**Бекенд:**
* **Python**
* **Django**

**База данни:**
* **PostgreSQL**

**Фронтенд:**
* **HTML**
* **CSS**
* **JavaScript**
* **Bootstrap** (ако си използвала)

## ⚙️ Инсталация и стартиране

Следвай тези стъпки, за да стартираш проекта локално:

1.  **Клонирай хранилището:**
    ```bash
    git clone [https://github.com/EliArn99/BookStore_Web_App.git](https://github.com/EliArn99/BookStore_Web_App.git)
    cd BookStore_Web_App
    ```
2.  **Създай виртуална среда и активирай я:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # За Linux/macOS
    # или
    venv\Scripts\activate  # За Windows
    ```
3.  **Инсталирай зависимостите:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Не забравяй да създадеш `requirements.txt` файл с `pip freeze > requirements.txt`)*
4.  **Настрой базата данни:**
    * Увери се, че имаш инсталиран PostgreSQL и създадена база данни.
    * Настрой `DATABASES` секцията във `settings.py` на Django, за да сочи към твоята PostgreSQL база данни.
    * Добави `.env` файл за чувствителна информация като `SECRET_KEY` и данни за базата данни.
5.  **Извърши миграциите:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Създай суперпотребител (по избор):**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Стартирай сървъра:**
    ```bash
    python manage.py runserver
    ```
    Приложението ще бъде достъпно на `http://127.0.0.1:8000/`.

## 📈 Научени уроци и предизвикателства

* Научих как да изграждам пълноценни уеб приложения с **Django**, включително модели, изгледи, темплейти и URL маршрутизация.
* Придобих опит в работата с **PostgreSQL** и оптимизирането на заявки за данни.
* Справих се с предизвикателства, свързани с **валидацията на потребителски вход** и **сигурността на данните**.

## 📝 Лиценз

Този проект е лицензиран под MIT License.

## ✉️ Контакти

Елица Арнаутска - [eli_arnaytska@abv.bg](mailto:eli_arnaytska@abv.bg)

[Моят GitHub профил](https://github.com/EliArn99)


