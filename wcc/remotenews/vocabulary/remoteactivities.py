from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from wcc.jsonapi.client import V10APIClient
import time
from plone.memoize import ram

class SearchableVocabulary(SimpleVocabulary):

    def search(self, query):
        return [
            t for t in self._terms if query.lower() in t.title.lower()
        ]

def _fivemins_cache_key(*args, **kwargs):
    return int(time.time()/300)

class RemoteActivities(grok.GlobalUtility):
    grok.name('wcc.remotenews.remoteactivities')
    grok.implements(IVocabularyFactory)

    @ram.cache(_fivemins_cache_key)
    def __call__(self, context):
        # XXX: should query default endpoint from registry
        endpoint = getattr(context, 'endpoint', 'http://www.oikoumene.org/api')
        client = V10APIClient(context, endpoint)

        terms = []
        activities = client.activities(limit=None)
        
        for activity in activities:
            terms.append(
                SimpleTerm(
                    value=activity['uuid'],
                    title=activity['title'], 
                    token=activity['uuid']
                )
            )
        return SearchableVocabulary(terms)
