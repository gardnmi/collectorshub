# Agent Changelog

## 2025-06-21 - Fixed Wishlist Toast and Count Updates
- Fixed wishlist count to update immediately using Out-Of-Band (OOB) swaps
- Improved toast notification styling with proper DaisyUI components
- Simplified wishlist action messages for better user experience
- Fixed message display on HTMX actions

## 2025-06-21 - Enhanced Real-time Wishlist Updates with HTMX
- Fixed wishlist count to update immediately when items are added/removed
- Integrated toast notifications to appear immediately via HTMX
- Added animations for toast messages (slide in, auto fade out)
- Improved HTMX implementation using HX-Trigger-After-Swap for more reliable updates
- Created reusable message partial template for consistent notification handling

## 2025-06-21 - Added Real-time Wishlist Count Update with HTMX
- Created a dedicated partial template for the wishlist count in the navbar
- Added HTMX event listener to update the count when wishlist items are added/removed
- Implemented a new `update_wishlist_count` view to handle the wishlist count updates
- Added loading indicators for wishlist buttons to improve user feedback
- Enhanced CSS for smoother transitions and loading states

## 2025-06-21 - Updated Wishlist Icon Display
- Modified the wishlist icon in the navbar to only show when there are items in the wishlist
- Updated wishlist_icon.html partial template for consistency

## 2025-06-21 - Added Wishlist Feature

### Created wishlist app:
- Created new Django app called 'wishlist'
- Defined the WishlistItem model to create wishlist functionality
- Added the app to the project's INSTALLED_APPS

### Created wishlist functionality:
- Added views for displaying, adding, and removing wishlist items
- Created templates for the wishlist pages and components
- Added wishlist icon to the navbar
- Integrated wishlist button on collectible detail pages
- Added wishlist tab on the user profile page

### Database changes:
- Created migrations for the WishlistItem model
- Created unique constraints to prevent duplicate wishlist entries

### User Interface improvements:
- Added wishlist indicator with count to the navigation bar
- Created tab interface on user profile to show wishlist items
- Added "Add to Wishlist" and "Remove from Wishlist" buttons on collectible detail pages
- Created dedicated page for viewing the full wishlist

### Integration:
- Updated collectible detail view to check if items are in the user's wishlist
- Updated the profile view to include wishlist items
- Added CSS for wishlist elements

## 2025-06-21 - Multi-Image Upload UI and Styling Fix
- Implemented Django's recommended MultipleFileInput/MultipleFileField for multi-image upload in CollectibleForm
- Updated collectible_form.html to wrap the file input in DaisyUI/Tailwind form-control, label, and help text for consistent styling
- Ensured file input is styled and works with multiple file selection, matching the rest of the form
