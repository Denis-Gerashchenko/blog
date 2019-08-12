# blog

The blog created with the Django

It may be used for an any advertisment and be managed via the admin site

The posts with a "Featured" checkbox turned on are placed on a main page.
The posts with a "Slider" checkbox turned on are placed on a slider

The both checkboxes can be used on the admin

There are the three roles:

- Author: can create and update the posts
- Moderator: can delete the comments
- Reader: can only write the comments

An author status should be given to a custom user within the django-admin

For a instagram panel on a sidebar there is a block in the page sidebar.html:38

{% instagram_user_recent_media <nstagram userprofile id> %}
  
It uses the instagram profile "nature" by a default

Feature:
The TinyMCE editor can be used to create and update the posts.
