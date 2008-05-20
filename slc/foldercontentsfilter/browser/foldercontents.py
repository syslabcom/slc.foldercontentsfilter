import Acquisition
from zope.interface import implements
from zope.app import pagetemplate 
from Products.CMFCore.utils import getToolByName
from plone.app.content.browser.foldercontents import FolderContentsView, FolderContentsTable
from plone.app.content.browser.tableview import Table, TableKSSView
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.memoize import instance
from Products.ATContentTypes.interface import IATTopic
from zope.component import getMultiAdapter

from Products.CMFPlone.interfaces import IPloneSiteRoot

import urllib


class FolderContentsFilterView(FolderContentsView):
    """ """
    implements(IFolderContentsView)

    def contents_table(self):
        """ allow to pass params to contentFilter """
        ploneUtils = getToolByName(self.context, 'plone_utils')
        friendly_types = ploneUtils.getUserFriendlyTypes()
        title = self.request.get('Title', '').strip()
        if title != '':
            title = title + '*'
        path = self.request.get('path', '')
        if title:
            contentFilter = { 'Title': title
                            , 'path': { 'query': path}
                            , 'portal_type': friendly_types
                            }
        else:
            contentFilter = {}
            sort_on = self.request.get('sort_on', 'getObjPositionInParent')
            contentFilter['sort_on'] = sort_on
            sort_order = self.request.get('sort_order', '')
            if sort_order:
                contentFilter['sort_order'] = sort_order
            
        table = FCFFolderContentsTable(self.context, 
                                    self.request, 
                                    contentFilter = contentFilter
                                   )
        return table.render()


    
class FCFFolderContentsTable(FolderContentsTable):
    """   
    The foldercontents table renders the table and its actions.
    """                

    def __init__(self, context, request, contentFilter={}):
        self.context = context
        self.request = request
        self.contentFilter = contentFilter

        url = self.context.absolute_url()
        view_url = url + '/@@folder_contents'
        self.table = FCFTable(request, url, view_url, self.items,
                           show_sort_column=self.show_sort_column,
                           buttons=self.buttons)   
                 
    @property
    @instance.memoize
    def items(self):
        """
        """
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_view = getMultiAdapter((self.context, self.request), name=u'plone')
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        portal_properties = getToolByName(self.context, 'portal_properties')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        site_properties = portal_properties.site_properties
        
        use_view_action = site_properties.getProperty('typesUseViewActionInListings', ())
        browser_default = self.context.browserDefault()
                
        if IATTopic.providedBy(self.context):
            contentsMethod = self.context.queryCatalog
        else:
            contentsMethod = portal_catalog
            path = {}
            path['query'] = "/".join(self.context.getPhysicalPath())
            if not (self.contentFilter.has_key('Title') or self.contentFilter.has_key('SearchableText')): 
                path['depth'] = 1
            self.contentFilter['path'] = path
            
        results = []
        for i, obj in enumerate(contentsMethod(self.contentFilter)):
            if (i + 1) % 2 == 0:
                table_row_class = "draggable even"
            else:
                table_row_class = "draggable odd"

            url = obj.getURL()
            path = obj.getPath or "/".join(obj.getPhysicalPath())
            icon = plone_view.getIcon(obj);
            
            type_class = 'contenttype-' + plone_utils.normalizeString(
                obj.portal_type)

            review_state = obj.review_state
            state_class = 'state-' + plone_utils.normalizeString(review_state)
            relative_url = obj.getURL(relative=True)
            obj_type = obj.portal_type

            modified = plone_view.toLocalizedTime(
                obj.ModificationDate, long_format=1)
            
            if obj_type in use_view_action:
                view_url = url + '/view'
            elif obj.is_folderish:
                view_url = url + "/folder_contents"              
            else:
                view_url = url

            is_browser_default = len(browser_default[1]) == 1 and (
                obj.id == browser_default[1][0])
                                 
            results.append(dict(
                url = url,
                id  = obj.getId,
                quoted_id = urllib.quote_plus(obj.getId),
                path = path,
                title_or_id = obj.pretty_title_or_id(),
                description = obj.Description,
                obj_type = obj_type,
                size = obj.getObjSize,
                modified = modified,
                icon = icon.html_tag(),
                type_class = type_class,
                wf_state = review_state,
                state_title = portal_workflow.getTitleForStateOnType(review_state,
                                                           obj_type),
                state_class = state_class,
                is_browser_default = is_browser_default,
                folderish = obj.is_folderish,
                relative_url = relative_url,
                view_url = view_url,
                table_row_class = table_row_class,
                is_expired = self.context.isExpired(obj),
            ))
        return results                 
                 
                           
    def render(self):
        render = self.table.render
        
        return self.table.render()


class FCFFolderContentsKSSView(TableKSSView):
    table = FCFFolderContentsTable
                
                

class FCFTable(Table):
    """   
    The table renders a table with sortable columns etc.

    It is meant to be subclassed to provide methods for getting specific table info.
    """                

    render = pagetemplate.ViewPageTemplateFile("templates/table.pt")
