# blog

Blog created with Django

May be used for any advertisment 

Posts with "Featured" checkbox turned on are placed on the main page.
Posts with "Slider" checkbox turned on are placed on a slider

Both checkboxes can be used on admin

There are three roles:

- Author: can create and update posts
- Moderator: can delete comments
- Reader: can only write comments

Author status should be given to custom user within django-admin

For instagram panel on sidebar there is a block in index.html:38

{% instagram_user_recent_media <nstagram userprofile id> %}
  
It uses "nature" by default
