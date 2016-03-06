# This is a chatfluence for Err plugins, use this to get started quickly.

from itertools import chain
import json
from PythonConfluenceAPI import ConfluenceAPI
import re

from errbot import BotPlugin, botcmd, webhook, re_botcmd, arg_botcmd

CONFIG_TEMPLATE = {
    'CONFLUENCE_USERNAME': 'changeme',
    'CONFLUENCE_PASSWORD': 'changeme',
    'CONFLUENCE_ENDPOINT': 'https://localhost',
    'CONFLUENCE_KEYSPACE': 'DS',
    'LIMIT': 10,
    }

class Chatfluence(BotPlugin):
    """An Err plugin chatfluence"""
    min_err_version = '2.0.0'  # Optional, but recommended
    max_err_version = '3.3.0'  # Optional, but recommended

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def activate(self):
        """Triggers on plugin activation"""

        self.log.debug(
            self.config['CONFLUENCE_USERNAME'],
            self.config['CONFLUENCE_PASSWORD'],
            self.config['CONFLUENCE_ENDPOINT']
        )

        self.api = ConfluenceAPI(
            self.config['CONFLUENCE_USERNAME'],
            self.config['CONFLUENCE_PASSWORD'],
            self.config['CONFLUENCE_ENDPOINT']
            )

        super(Chatfluence, self).activate()

    @botcmd()
    def recent(self, mess, args):
        """A command that shows recent blog posts.
        Optionally pass in a result limit."""

        if args:
            limit = args
        else:
            limit = self.config['LIMIT']


        results = self._recent(limit=limit)

        endpoint = self.config['CONFLUENCE_ENDPOINT']

        for result in results:
                posted = self._get_posted_date(result['id'])[:10]

                line = '{0} {1} {2}{3}'.format(
                    posted,
                    result['title'],
                    endpoint.rstrip('/'),
                    result['_links']['tinyui']
                )
                yield line

    def _recent(self, limit=None, space=None):
        """Method to fetch recent blog posts wihtin a space."""

        if not limit:
            limit = self.config['LIMIT']

        if not space:
            space = self.config['CONFLUENCE_KEYSPACE']

        recent = self.api.get_content(
            content_type='blogpost',
            space_key=space,
            limit=limit,
        )

        return recent['results']

    @botcmd()
    def search(self, mess, args):
        """A command that searches confluence.
        This uses the CQL language. https://developer.atlassian.com/confdev/confluence-rest-api/advanced-searching-using-cql
        """

        if '=' not in str(args) and '~' not in str(args):
            cql = 'text ~ "{0}"'.format(args)
        else:
            cql = str(args)

        # remove slack's smart quotes
        cql = cql.replace('“', '"').replace('”', '"')

        self.log.debug('search: {0}'.format(cql))

        results = self._search(cql)

        for result in results:
                posted = self._get_posted_date(result['id'])[:10]

                line = '{0} {1}'.format(
                    posted,
                    result['title'],
                )
                yield line
                self.log.debug(result)


    def _search(self, cql, limit=None):
        """Searches confluence."""

        if not limit:
            limit = self.config['LIMIT']

        results = self.api.search_content(
            cql_str=cql,
            limit=limit
        )
        return results['results']



    def _get_posted_date(self, pageid):
        """Gets date content was created"""

        page = self.api.get_content_by_id(content_id=pageid)
        posted = page['history']['createdDate']

        return posted


    # TODO: can these patterns come from the configuration?
    @re_botcmd(pattern=r"(^| )@news?( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_news(self, msg, match):
        """Mention @news and I will blog it."""

        content = 'Posted by {0}:  \n {1}'.format(msg.frm, msg.body)

        title = ' '.join(msg.body.split()[0:5])
        keyspace = self.config['CONFLUENCE_KEYSPACE']

        result = self._post(title, content, keyspace)

        return result

    def _post(self, title, content, space):
        """Method to make a blog post in a space."""

        try:
            r = self.api.create_new_content({
                'type': 'blogpost',
                'title': title,
                'space': {'key': space},
                'body': {
                    'storage': {'value': content,
                                'representation': 'storage'
                                }
                }
            })
            self.log.debug(r)
            line = 'POSTED: {0} {1} {2}/{3}'.format(
                r['history']['createdDate'][:10],
                r['title'],
                r['_links']['base'],
                r['_links']['tinyui'],
            )

        except Exception as e:
            self.log.critical(e)


        return line
