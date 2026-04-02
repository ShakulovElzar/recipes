# Recipe Sharing and Meal Planning

A full-stack Django web application for sharing recipes, browsing community posts, building a personal profile, and organizing meals in a monthly planner.

## Overview

This project is a community-driven recipe platform where users can:

* browse recipes shared by other users
* publish their own recipes with images and rich text content
* like recipes
* comment on recipe pages
* manage a personal profile with avatar and bio
* create a personal meal plan by assigning recipes to breakfast, lunch, or dinner slots

The application is built with Django and uses MySQL as its database backend. It also integrates Django Allauth for authentication, Crispy Forms with Bootstrap 5 for form rendering, and rich text/image utilities for better content management.

## Main Features

### Home page

* shows a landing page for the platform
* highlights the 3 most-viewed recipes
* includes calls to action for browsing recipes or sharing a recipe

### Recipe system

* view all recipes in a list page
* search recipes by title, description, instructions, ingredients, cuisine type, or meal type
* open a recipe detail page
* automatically increase the recipe view counter when a detail page is opened
* create a new recipe
* edit your own recipe
* delete your own recipe
* like and unlike recipes
* upload recipe images
* store structured recipe information such as:

  * title
  * description
  * ingredients
  * instructions
  * meal type
  * cuisine type
  * calories
  * image and alt text

### Comments

* authenticated users can post comments on recipe detail pages
* recipe owners and superusers can manage moderation through delete permissions for comments
* success and error messages are displayed for comment actions

### User profiles

* automatic profile creation when a new user account is created
* custom user profile with:

  * avatar image
  * bio
* profile page showing:

  * member since date
  * total number of recipes published by the user
  * user bio
  * all recipes created by the user
* users can edit only their own profile

### Meal planner

* login-protected meal planner page
* monthly meal planning layout based on the current month
* assign recipes to meal slots such as breakfast, lunch, and dinner
* optional filtering by calories and search query when selecting a meal
* random recipe suggestion from filtered results
* save or update a meal entry for a specific date and meal type

### Authentication

* registration and sign in handled with Django Allauth
* support for login by username or email
* logout and profile access in the navigation

## Tech Stack

### Backend

* Python
* Django 6
* MySQL

### Frontend

* Django Templates
* HTML
* CSS
* Bootstrap 5

### Packages and integrations

* `django-allauth` for authentication
* `django-crispy-forms` and `crispy-bootstrap5` for styled forms
* `djrichtextfield` for rich text editing
* `django-resized` for automatic image resizing and WebP conversion
* `django-reorder` for custom meal ordering in the planner
* `Pillow` for image processing

## Project Structure

```text
recipes/
├── home/                 # Landing page app
├── main/                 # Project settings and root URLs
├── meal_planner/         # Monthly meal planning app
├── media/                # Uploaded user and recipe images
├── profiles/             # User profiles app
├── recipes/              # Recipe CRUD, likes, comments, search
├── static/               # Static assets
├── templates/            # Global templates, base layout, includes, auth templates
├── manage.py
└── requirements.txt
```

## Apps Breakdown

### `main`

Contains global project configuration:

* settings
* root URL routing
* media/static setup
* authentication backend configuration
* MySQL database connection

### `home`

Responsible for the landing page.

Key behavior:

* displays the top 3 recipes ordered by views

### `recipes`

Core app of the platform.

Models:

* `Recipe`
* `Comment`

Main responsibilities:

* list recipes
* search recipes
* create recipe
* update recipe
* delete recipe
* recipe detail page
* recipe likes
* comments

### `profiles`

Handles user profile data and editing.

Model:

* `Profile`

Main responsibilities:

* create profile automatically on user creation
* display profile page
* update profile data

### `meal_planner`

Handles monthly meal planning.

Model:

* `Meal`

Main responsibilities:

* show planner for the current month
* generate filtered recipe suggestions
* assign selected recipes to meal slots

## Database Models

### Recipe

Represents a recipe submitted by a user.

Fields include:

* `user`
* `title`
* `description`
* `instructions`
* `ingredients`
* `image`
* `image_alt`
* `meal_type`
* `cuisine_type`
* `calories`
* `views`
* `likes`
* `posted_date`

### Comment

Represents a comment posted under a recipe.

Fields include:

* `recipe`
* `user`
* `body`
* `created_on`
* `updated_on`

### Profile

Represents extra information attached to a user account.

Fields include:

* `user`
* `image`
* `bio`

### Meal

Represents a planned meal for a user on a specific date.

Fields include:

* `user`
* `recipe`
* `meal_type`
* `meal_date`

## URL Overview

### Root routes

* `/` → home page
* `/recipes/` → recipes app
* `/profile/` → profiles app
* `/meal_planner/` → meal planner app
* `/accounts/` → authentication routes via Allauth
* `/admin/` → Django admin panel

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ShakulovElzar/recipes.git
cd recipes
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

#### macOS / Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create an `env.py` file in the project root or configure environment variables in your system.

Expected values:

```python
import os

os.environ.setdefault("SECRET_KEY", "your-secret-key")
os.environ.setdefault("DB_NAME", "your-database-name")
os.environ.setdefault("DB_USER", "your-database-user")
os.environ.setdefault("DB_PASSWORD", "your-database-password")
os.environ.setdefault("DB_HOST", "127.0.0.1")
os.environ.setdefault("DB_PORT", "3306")
```

### 5. Create the MySQL database

Example:

```sql
CREATE DATABASE recipes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Authentication Setup

The project uses Django Allauth.

Current behavior includes:

* login by username or email
* signup with email, username, and password
* no email verification required in development
* redirect to home page after login

## Media and Static Files

### Static files

Static assets are loaded from the `static/` directory.

### Media files

Uploaded images are stored in the `media/` directory.

The project is configured to serve media files automatically when `DEBUG=True`.

## Form and Editor Features

* Crispy Forms is used for cleaner Bootstrap-based form rendering
* Rich text fields are used for recipe ingredients, recipe instructions, and profile bio
* CKEditor is loaded through `djrichtextfield`
* uploaded profile and recipe images are resized and converted to WebP

## Search Functionality

The recipes page supports search across multiple fields:

* title
* description
* instructions
* ingredients
* cuisine type
* meal type

The meal planner also supports filtering recipes by:

* free-text search
* calorie limit
* selected meal type

## Permissions and Access Rules

### Recipe permissions

* any visitor can browse recipes
* only authenticated users can create recipes
* only the recipe owner can edit or delete their own recipe
* users cannot like their own recipe

### Profile permissions

* all visitors can view profile pages
* only the owner can edit their profile

### Comment permissions

* authenticated users can post comments
* a comment can be deleted by its owner or a superuser

### Meal planner permissions

* meal planner page requires login
* meals are intended to be personal to the logged-in user

## UI Structure

The project uses a shared `base.html` template with:

* reusable header
* reusable footer
* content blocks for each page
* navigation links for home, recipes, profile, login/logout, and recipe creation

## Known Improvements / Future Enhancements

Potential next steps for the project:

* improve URL patterns for cleaner and fully validated dynamic routes
* add pagination on recipe listing pages
* add recipe categories and tags
* add bookmark or favorites feature
* add full meal planner CRUD controls from the planner page
* add profile cover images and richer user stats
* add email verification for production
* add test coverage for views, forms, and models
* add deployment configuration for production environments
* improve accessibility and responsive styling

## Notes for Developers

A few implementation details worth knowing:

* MySQL is required by the current settings file
* `env.py` is optionally imported if present
* media serving is only configured automatically in development mode
* profile records are created automatically through a post-save signal on the Django `User` model
* the home page uses recipe view counts to determine featured recipes

## Example User Flow

1. A visitor signs up for an account.
2. A profile is created automatically.
3. The user logs in.
4. The user creates a new recipe with ingredients, instructions, calories, and image.
5. Other users browse the recipe list and open the recipe detail page.
6. View count increases automatically.
7. Users can like the recipe and leave comments.
8. The recipe owner can edit or delete the recipe later.
9. A logged-in user can visit the meal planner and assign recipes to dates and meal slots.

## Requirements

Main packages currently used in the project include:

* Django
* django-allauth
* django-crispy-forms
* crispy-bootstrap5
* django-reorder
* django-resized
* django-richtextfield
* Pillow

See `requirements.txt` for the full dependency list.

## License

No license has been added to this repository yet. If you plan to share or deploy the project publicly, consider adding a license file.

## Author

Created by **ShakulovElzar**.
