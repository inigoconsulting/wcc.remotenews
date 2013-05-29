from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.multilingualbehavior.directives import languageindependent
from wcc.remotenews import MessageFactory as _


# Interface class; used to define content-type schema.

class IRemoteNewsFolder(form.Schema, IImageScaleTraversable):
    """
    A folder displaying news from remote API
    """

    languageindependent('endpoint')
    endpoint = schema.TextLine(
        title=_(u'API Endpoint'),
        default=u'http://www.oikoumene.org/api'
    )

    languageindependent('q_category')
    q_category = schema.TextLine(
        title=_(u'Category'),
        description=(
            u"Category (subject) tag to query for. Leave blank to " 
            u"query for all news"
        ),
        required=False
    )

    q_language = schema.TextLine(
        title=_(u'Language code'),
        description=u'Language code to import the news from. Leave blank to use current language',
        default=u'',
        required=False
    )




