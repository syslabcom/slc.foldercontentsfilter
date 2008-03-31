from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import SearchBoxViewlet

class FolderContentsSearchBoxViewlet(SearchBoxViewlet):
    render = ViewPageTemplateFile('templates/searchbox.pt')