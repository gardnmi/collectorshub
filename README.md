# CollectorsHub

A Django-based web application for collectors to showcase, manage, and potentially trade collectible items.

## Features

### Core Features
- User authentication with django-allauth
- Create and manage user profiles
- List and browse collectible items
- Search and filter collectibles
- Item categorization

### Advanced Features
- Wishlist functionality for saving items of interest
- AI-powered collectible description enhancement
- Modern UI with TailwindCSS and DaisyUI
- Interactive UI elements using HTMX

## Technology Stack

- **Backend**: Python 3.13+, Django 5.2+
- **Frontend**: TailwindCSS, DaisyUI, HTMX
- **Package Management**: UV
- **Authentication**: django-allauth with allauth-ui
- **Admin Interface**: Unfold
- **Development Tools**: django-extensions, django-cotton, django-vite

## Getting Started

### Prerequisites
- Python 3.13+
- UV package manager

### Installation

1. Clone the repository
```bash
git clone git@github.com:yourusername/collectorshub.git
cd collectorshub
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies using UV
```bash
pip install uv
uv pip install -r requirements.txt
```

4. Apply migrations
```bash
uv run manage.py migrate
```

5. Create a superuser
```bash
uv run manage.py createsuperuser
```

6. Run the development server
```bash
uv run manage.py runserver
```

## Usage

1. Browse collectibles on the main page
2. Create an account or log in to manage your collectibles
3. Add items to your wishlist by clicking the heart icon
4. View your wishlist from your profile or the wishlist icon in the navigation bar
5. Contact other collectors about items in your wishlist (coming soon)

## Project Structure

- **accounts/** - User profile management
- **collectibles/** - Core collectibles functionality
- **wishlist/** - Wishlist management
- **templates/** - Global templates
- **static/** - Static files (CSS, JS)
