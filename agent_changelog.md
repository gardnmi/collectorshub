# Agent Changelog

## 2025-06-22 - Toast Notification Improvements

- Fixed issue where toasts (Django messages) would stack up and persist on the conversation page.
- Added auto-dismiss script to fade out and remove toasts after 4 seconds for a cleaner user experience.
- Disabled toast notifications specifically on the conversation detail page to prevent message toasts from appearing for every chat message.
- Toasts continue to work as expected on all other pages.

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

## 2025-06-21 - DaisyUI Carousel Modal Navigation Fix
- Updated collectible detail modal carousel to use DaisyUI's pure HTML anchor-based navigation
- Removed custom JavaScript for carousel navigation; now uses only DaisyUI and Django template logic
- Fixed left/right arrow logic so carousel wraps correctly and navigation is smooth for all images
- Removed 'Primary' and 'Secondary' badges from below images in the collectible detail modal carousel for a cleaner, distraction-free image browsing experience.

## 2025-06-21 - Profile Page Image Display Update
- Updated `accounts/templates/accounts/profile.html` to use the new `CollectibleImage` model for displaying images on collectible and wishlist cards. The template now fetches the primary image (or first image) from the related images set, matching the logic in `collectible_list.html`. This removes legacy references to the old single-image field and ensures consistent image display across the app after the multi-image refactor.
- Updated `wishlist/templates/wishlist/wishlist.html` to use the new `CollectibleImage` model for displaying images on wishlist cards. The template now fetches the primary image (or first image) from the related images set, matching the logic in `profile.html` and `collectible_list.html`. This ensures consistent image display after the multi-image refactor.
- Updated the 'View Full Wishlist' button in the profile page's wishlist tab to use 'btn-primary btn-sm' for consistent color and style with other action buttons on the page.

## 2025-06-21 - User-to-User Messaging System (HTMX, DaisyUI, Django)

- Scaffolded new Django app `messaging` with models: `Conversation` (participants, optional item), `Message` (sender, text, attachment, is_offer, offer_amount).
- Registered `Conversation` and `Message` in Unfold admin.
- Created `MessageForm` for sending messages/offers, using Tailwind/DaisyUI classes.
- Implemented views:
  - `inbox` (list conversations)
  - `conversation_detail` (view/send messages, HTMX support)
  - `start_conversation` (initiate conversation, item-specific or general)
- Added templates:
  - `inbox.html` (DaisyUI card list)
  - `conversation_detail.html` (DaisyUI chat UI, message form, HTMX-ready, uses `_messages_list.html` partial)
  - `start_conversation.html` (item and seller info, user_id only for general)
  - `_messages_list.html` (partial for rendering messages, with correct Django template logic)
- Registered messaging app in `INSTALLED_APPS` and added its URLs to the main project with the correct namespace.
- Added "Messages" button to main navbar for authenticated users, linking to messaging inbox.
- Added "Contact Seller" button to collectible detail pages for authenticated users (not the owner), styled with DaisyUI, linking to start_conversation for the item.
- Improved start_conversation so that when accessed from an item, it auto-selects the seller and hides the user_id field.
- Fixed Django template errors (replaced Python inline if/else with Django template logic in all messaging templates).
- Added POST handling to `conversation_detail`: on HTMX request, only the messages list partial is returned to avoid HTML duplication; on normal POST, redirect.
- Updated form rendering to use direct field output (no crispy forms), with Tailwind/DaisyUI classes.
- All messaging templates now use correct Django template logic and are HTMX-ready for smooth chat experience.

## 2025-06-21 - Messaging UI/UX Improvements

- Updated `MessageForm` to use a resizable textarea for the message input, improving usability for longer messages.
- Rearranged the conversation form in `conversation_detail.html` so the message box is on top, with file upload, offer checkbox, offer amount, and send button below for a cleaner layout.
- Improved `_messages_list.html` to only render the sender's profile image if it exists, preventing broken or empty avatars and matching the actual profile model field (`profile_image`).
- All changes follow TailwindCSS and DaisyUI conventions for consistent styling.
