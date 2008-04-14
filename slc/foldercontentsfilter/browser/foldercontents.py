import Acquisition
from zope.interface import implements
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.app import pagetemplate 

from plone.app.content.browser.foldercontents import FolderContentsView, FolderContentsTable
from plone.app.content.browser.tableview import Table, TableKSSView
from plone.app.content.browser.interfaces import IFolderContentsView


class FolderContentsFilterView(FolderContentsView):
    """ """
    implements(IFolderContentsView)

    def contents_table(self):
        """ allow to pass params to contentFilter """
        title = self.request.get('Title', '').strip()
        if title != '':
            title = title + '*'
        path = self.request.get('path', '')
        #depth = self.request.get('depth',1)
        if title:
            contentFilter = { 'Title': title
                            , 'path': { 'query': path}
#                                      , 'depth': depth}
                            }
        else:
            contentFilter = {}
            
        sort_on = self.request.get('sort_on', 'sortable_title')
        if sort_on!='':
            contentFilter['sort_on'] = sort_on

        sort_order = self.request.get('sort_order', '')
        if sort_order!='':
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
