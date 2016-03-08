err-chatfluence
===============

This plugin will connect err to a Confluence instance and space. The primary focus is
on managing a blog within a Confluence space, but it can (and will) be extended to 
do much more.

### Installation

See http://errbot.io/en/latest/user_guide/setup.html for instructions on getting errbot up
and running. Do that first, then come back here.

I assume that you have `BOT_PREFIX_OPTIONAL_ON_CHAT = True` in your configuration. If not,
you will need to add in your bot prefix (often it's an exclamation point `!`).

Once you have errbot running, from a direct chat with your bot (as an admin) give this command:

`repos install https://github.com/ytjohn/err-chatfluence.git`

You should see it install. Because it's not configured, you will probably get an error 
message. It should look like this:

```
A new plugin repository has been installed correctly from https://github.com/ytjohn/err-chatfluence.git. Refreshing the plugins commands...
Error: Chatfluence failed to start : 'NoneType' object is not subscriptable
Error: Chatfluence failed to start : 'NoneType' object is not subscriptable
```

### Configuration

This plugin requires that you configure a username, password, and endpoint URL for your
Confluence installation. All actions with Chatfluence goes to a default keyspace that you
configure.

You will probably need to reload the plugin after it starts.



    !plugin config Chatfluence 
    {'CONFLUENCE_ENDPOINT': 'https://localhost',
    'CONFLUENCE_KEYSPACE': 'DS',
    'CONFLUENCE_PASSWORD': 'changeme',
    'CONFLUENCE_USERNAME': 'changeme',
    'LIMIT': 10}
    
    !plugin reload Chatfluence


If you have a Atlassian hosted JIRA (on-demand), your ENDPOINT will be the custom subdomain, 
followed by /wiki/. For example: **https://example.atlassian.net/wiki/**.


Licence
-------

err-chatfluence is free software released under GPL version 3. Please see COPYING for full 
license text.
