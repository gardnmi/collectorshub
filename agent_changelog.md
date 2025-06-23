# Agent Changelog

## 2025-06-23 - Wishlist, Offer, and Profile Cleanup

- Removed the "My Wishlist" tab and all supporting backend code from the user profile page for a cleaner UX
- Updated wishlist page: "Contact Seller" button now says "Make Offer" for each item
- Added support for making offers on the entire wishlist, opening a conversation linked to all wishlist items
- Conversations for wishlist offers now show all related collectibles and the total, using the same message form as single-item offers (no pre-filled text)
- Refactored backend to remove all redundant wishlist context from the profile view
- Fixed template errors and improved context passing for wishlist conversations

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

## 2025-06-22 - Messaging Character Limit

- Added a 1000-character limit to messages in the messaging system.
- Enforced the limit both in the form widget (`maxlength` attribute) and with server-side validation in `MessageForm`.
- Users now receive a clear error if they attempt to send a message longer than 1000 characters.

## 2025-06-21 - Messaging UI/UX Improvements

- Updated `MessageForm` to use a resizable textarea for the message input, improving usability for longer messages.
- Rearranged the conversation form in `conversation_detail.html` so the message box is on top, with file upload, offer checkbox, offer amount, and send button below for a cleaner layout.
- Improved `_messages_list.html` to only render the sender's profile image if it exists, preventing broken or empty avatars and matching the actual profile model field (`profile_image`).
- All changes follow TailwindCSS and DaisyUI conventions for consistent styling.

## 2025-06-22 - Messaging Offer UI Simplification

- Removed the "Offer?" checkbox from the message form; users now simply enter an amount in the offer field if they want to make an offer.
- Changed the offer amount field's placeholder to "Make an Offer" for clarity.
- Messages with an offer amount are now automatically highlighted as offers in the conversation UI.
- Cleaned up template logic and removed unsupported template filters for compatibility.

## 2025-06-22 - Messaging Admin Cleanup

- Removed the obsolete `is_offer` field from `MessageAdmin` in the Django admin.
- Updated `list_display` and `list_filter` to use `offer_amount` and `is_read` for better admin usability and to resolve system check errors.

## 2025-06-22 - Messaging Navbar Icon and Unread Badge

- Replaced the "Messages" button in the navbar with a clear envelope/message icon for better recognition.
- Added a "NEW" badge to the icon when there are unread messages for the user.
- The unread badge now appears on every page with the navbar, not just the inbox, by passing `unread_count` to all relevant templates.
- Improved backend logic to ensure unread message count is always accurate and up-to-date.

## 2025-06-22 - Global Unread Message Badge via Context Processor

- Added a custom context processor (`messaging.context_processors.unread_message_count`) to make `unread_count` available in all templates for authenticated users.
- The "NEW" badge on the messages icon in the navbar now appears on every page, not just messaging-related views.
- Ensured the unread message count is always accurate and globally accessible for a consistent user experience.

## 2025-06-22 - Messaging Inbox: Unread Conversations at Top, Badge Icon

- Updated the `inbox` view in `messaging/views.py` to annotate each conversation with unread status for the current user and sort conversations so unread ones appear at the top.
- Refactored the context passed to the inbox template: now uses `convo_list` (with `convo`, `unread`, and `last_updated` for each conversation) instead of the old `conversations` queryset.
- Updated `messaging/templates/messaging/inbox.html` to:
  - Use `convo_list` for rendering conversations.
  - Display a "NEW" badge with an icon (DaisyUI badge + SVG) next to any conversation with unread messages.
  - Ensure the UI is clear and modern, matching the rest of the app's DaisyUI/Tailwind style.
  - This makes it easy for users to spot new conversations and ensures the most relevant chats are always at the top of their inbox.

## 2025-06-22 - Messaging Conversation: Auto-Scroll to Latest Message

- Added a JavaScript snippet to `messaging/templates/messaging/conversation_detail.html` that automatically scrolls the message list to the bottom when the page loads.
- This ensures users always see the newest messages first and can scroll up to view older history, providing a modern chat experience.
- No backend changes required; the update is purely in the template for a smoother user experience.

## 2025-06-22 - Major Project Structure Refactor and UI Improvements

- Renamed all Django app folders to use the `a_` prefix (e.g., `accounts` → `a_accounts`, `collectibles` → `a_collectibles`, etc.) and main project to `a_core`.
- Updated all references in `INSTALLED_APPS`, `ROOT_URLCONF`, `WSGI_APPLICATION`, and context processors in `a_core/settings.py` to use new app names.
- Updated all import statements and dynamic imports in code to use new app names (e.g., `a_wishlist.models`).
- Updated all `include()` references in `a_core/urls.py` to use new app names.
- Fixed import and context processor errors for `a_messaging` and `a_wishlist`.
- Improved the collectibles list page to display a visible title "All Collectibles" at the top.
- Replaced the "Profile" button in the navbar with the user's profile image or a placeholder avatar, linking to the profile page.
- Enhanced the default profile avatar: made it larger, perfectly centered, and visually consistent with the rest of the UI.
- Adjusted the vertical alignment of the default profile avatar for better appearance.

## 2025-06-22 - Sample Data Generation and Category Initialization Refactor

- Added a management command `generate_sample_collectibles` to quickly generate 120+ sample collectibles for testing, with random names, prices, conditions, and categories (no images).
- Moved the default category creation logic out of the models and into the management command, so running the command will always ensure categories exist before generating collectibles.
- Cleaned up `a_collectibles/models.py` by removing the post-migrate signal and category initialization logic.
- Fixed all dynamic imports and references to use the new app names (e.g., `a_wishlist.models`) throughout the codebase, including in `a_collectibles/views.py` and `a_accounts/views.py`.
- The collectibles detail view and other related features now work correctly with the new app structure and dynamic import logic.

## 2025-06-22 - Messaging Namespace and URL Refactor

- Updated all Django template `{% url %}` tags and reverse lookups for the messaging app to use the new `a_messaging` namespace after the app folder rename.
- Changed `app_name = "messaging"` to `app_name = "a_messaging"` in `a_messaging/urls.py` for correct namespacing.
- Updated all messaging-related links in templates (navbar, conversation, inbox, etc.) to use `a_messaging:` instead of `messaging:`.
- Verified and fixed all dynamic and static imports for wishlist and messaging to use the new app names (e.g., `a_wishlist.models`).
- Cleaned up category initialization logic and ensured sample data generation is robust for testing with large numbers of collectibles.

## 2025-06-22 - Wishlist and Collectibles UI/UX Improvements

- Collectibles list page:
  - Added "Add to Wishlist" button to each card, using a custom template filter to show "Remove from Wishlist" if already in wishlist.
  - Button state updates instantly with HTMX when adding/removing, without page reload.
  - Disabled toast notifications on this page for a cleaner experience.
- Wishlist page:
  - Grouped "View Details", "Contact Seller", and "Remove" buttons in a single row for better appearance.
  - Aligned "View Details" to the left, with "Contact Seller" and "Remove" on the right.
  - When removing an item, the card stays and the button flips to "Add to Wishlist" (undo), rather than removing the card.
  - Disabled toast notifications on this page as well.
- Profile wishlist tab:
  - Fixed button alignment and improved consistency with wishlist page.
- Added a custom template filter (`in_wishlist`) in `a_collectibles/templatetags` to check if a collectible is in the user's wishlist.
- Refactored `remove_from_wishlist` view to support button-only swaps for wishlist page, keeping cards visible.

## 2025-06-22 - Wishlist Navbar Count OOB Update

- Fixed wishlist count icon in the navbar to update instantly when adding or removing items from the wishlist page, using HTMX out-of-band (OOB) swaps.
- Now, the wishlist count stays accurate and in sync across all pages, including when using the undo/add-back button on the wishlist page.

## 2025-06-22 - Made Collectible Card Images Clickable

- Made collectible card images on the collectibles list page clickable, linking to the collectible detail page. The image is now wrapped in an anchor tag pointing to the detail view, with hover and cursor-pointer styling for clear affordance.

## 2025-06-22 - Clickable Preview Card Images Everywhere

- Made collectible preview card images clickable everywhere they appear:
  - Collectibles list page
  - Wishlist page
  - Profile page (both user's collectibles and wishlist tabs)
- Images now link to the collectible detail page and have pointer/hover affordance for clarity.

## 2025-06-22 - Back to List Button UX Fix

- Reverted the "Back to List" button on the collectible detail page to a regular link (instead of using `window.history.back()`), ensuring it always returns to the collectibles list in one click.
- This avoids confusion caused by modal carousel navigation adding history entries, which previously required multiple clicks to return to the list.
- The button now provides a consistent and intuitive navigation experience for users.

## 2025-06-23 - Collectible Category Improvements

- Added a "Add New Category" field to the collectible create/update form. Users can now enter a new category name directly on the form; it will be created and added to the collectible automatically.
- Made the categories field optional in the collectible form.
- Updated the collectible detail page to display all categories as badges. If no categories are set, it shows "None".
