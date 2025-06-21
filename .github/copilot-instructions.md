# Copilot Instructions for CollectorsHub Project

## Project Overview
CollectorsHub is a Django-based web application for collectors to showcase, manage, and potentially trade collectible items. The project leverages modern web technologies like HTMX for interactive experiences without heavy JavaScript, TailwindCSS with DaisyUI for styling, and various Django extensions for enhanced functionality.

## Technology Stack
- **Backend**: Python 3.13+, Django 5.2+
- **Frontend**: TailwindCSS, DaisyUI, HTMX
- **Package Management**: UV
- **Authentication**: django-allauth with allauth-ui
- **Admin Interface**: Unfold (preferred over Django's built-in admin)
- **Development Tools**: django-extensions, django-cotton, django-vite

## Coding Guidelines

### General Principles
- Prefer function-based views over class-based views when possible
- Use HTMX for interactive UI elements instead of JavaScript
- Leverage Django's built-in features and included extensions before adding new dependencies
- Follow Django's best practices for project structure and organization

### Python Specific
- Use Python 3.13+ features when appropriate
- Write type hints for functions and method signatures
- Format code according to PEP 8 guidelines
- Use docstrings for functions and classes

### Django Specific
- Use Unfold for admin customizations rather than the default Django admin
- Leverage django-extensions for enhanced development tooling
- Use django-allauth-ui for authentication templates and flow
- Organize code into appropriate apps based on functionality
- Prefer django-htmx decorators and middleware for HTMX interactions

### Frontend
- Use TailwindCSS utilities directly in templates
- Leverage DaisyUI components for consistent UI elements
- Minimize custom CSS; prefer composing with existing Tailwind utilities
- Use HTMX attributes directly in templates for interactive elements
- Use django-vite for asset bundling when needed

### Database
- Create models with clear relationships and appropriate field types
- Use Django migrations to manage database schema changes
- Add indexes for fields used in filtering or ordering
- Consider using Django's select_related and prefetch_related for optimization

### Authentication and Authorization
- Use django-allauth for authentication flows
- Implement proper permission checks for views
- Consider using Django's built-in permission system

## HTMX Usage Patterns
- Prefer partial template rendering over full page reloads
- Use hx-get, hx-post, hx-put, hx-delete for AJAX requests
- Use hx-swap for DOM manipulation
- Use hx-trigger for event handling
- Consider using hx-boost for progressive enhancement

## Project Structure Recommendations
- Keep apps focused on specific functionality
- Use templates directory structure that mirrors app structure
- Maintain a consistent URL naming scheme
- Place business logic in services or model methods, not in views
- Log your changes in agent_changelog.md for tracking modifications

## Deployment Considerations
- Use whitenoise for static file serving in production
- Consider uvicorn for ASGI server deployment
- Use environment variables for configuration via python-decouple
- Ensure DEBUG is set to False in production

## Additional Recommendations
- Use cotton for component-based templates
- Consider LLM integration for AI-enhanced features
- Leverage django-widget-tweaks for form customization without custom form classes
- Use django-unfold's ModelAdmin for consistent admin styling