# -*- coding: utf-8 -*-
"""Default Page CMS widgets."""
from os.path import join
from django.conf import settings
from django.forms import TextInput, Textarea
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.template.loader import render_to_string
from pages.settings import PAGES_MEDIA_URL, PAGE_TAGGING, PAGE_TINYMCE
from pages.models import Page

if PAGE_TAGGING:
    from tagging.models import Tag
    from django.utils import simplejson

    class AutoCompleteTagInput(TextInput):
        """An autocompete widget"""
        class Media:
            js = [join(PAGES_MEDIA_URL, path) for path in (
                'javascript/jquery.js',
                'javascript/jquery.bgiframe.min.js',
                'javascript/jquery.ajaxQueue.js',
                'javascript/jquery.autocomplete.min.js'
            )]

        def render(self, name, value, attrs=None):
            rendered = super(AutoCompleteTagInput, self).render(name, value, attrs)
            page_tags = Tag.objects.usage_for_model(Page)
            context = {
                'name': name,
                'tags': simplejson.dumps([tag.name for tag in page_tags], ensure_ascii=False),
            }
            return rendered + mark_safe(render_to_string(
                'admin/pages/page/widgets/autocompletetaginput.html', context))

class RichTextarea(Textarea):
    """A RichTextarea widget."""
    class Media:
        js = [join(PAGES_MEDIA_URL, path) for path in (
            'javascript/jquery.js',
        )]
        css = {
            'all': [join(PAGES_MEDIA_URL, path) for path in (
                'css/rte.css',
            )]
        }

    def __init__(self, attrs=None):
        attrs = {'class': 'rte'}
        super(RichTextarea, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(RichTextarea, self).render(name, value, attrs)
        context = {
            'name': name,
            'PAGES_MEDIA_URL': PAGES_MEDIA_URL,
        }
        return rendered + mark_safe(render_to_string(
            'admin/pages/page/widgets/richtextarea.html', context))

if PAGE_TINYMCE:
    from tinymce import widgets as tinymce_widgets
    
    class TinyMCE(tinymce_widgets.TinyMCE):
        """TinyMCE widget."""
        def __init__(self, content_language=None, attrs=None, mce_attrs={}):
            self.mce_attrs = mce_attrs
            self.mce_attrs.update({
                'mode': "exact",
                'theme': "advanced",
                'width': 640,
                'height': 400,
                'theme_advanced_toolbar_location': "top",
                'theme_advanced_toolbar_align': "left"
            })
            super(TinyMCE, self).__init__(content_language, attrs, mce_attrs)

class WYMEditor(Textarea):
    """WYMEditor widget."""

    class Media:
        js = [join(PAGES_MEDIA_URL, path) for path in (
            'javascript/jquery.js',
            'wymeditor/jquery.wymeditor.js',
            'wymeditor/plugins/resizable/jquery.wymeditor.resizable.js',
        )]
        
        if "filebrowser" in getattr(settings, 'INSTALLED_APPS', []):
            js.append(join(PAGES_MEDIA_URL, 'wymeditor/plugins/filebrowser/jquery.wymeditor.filebrowser.js'))
        

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'wymeditor'}
        if attrs:
            self.attrs.update(attrs)
        super(WYMEditor, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(WYMEditor, self).render(name, value, attrs)
        context = {
            'page_list':Page.objects.all().order_by('tree_id'),
            'name': name,
            'language': self.language,
            'PAGES_MEDIA_URL': PAGES_MEDIA_URL,
        }
        
        context['filebrowser'] = 0
        if "filebrowser" in getattr(settings, 'INSTALLED_APPS', []):
            context['filebrowser'] = 1
            
        return rendered + mark_safe(render_to_string(
            'admin/pages/page/widgets/wymeditor.html', context))

class markItUpMarkdown(Textarea):
    """markItUpMarkdown widget."""
    
    class Media:
        js = [join(PAGES_MEDIA_URL, path) for path in (
            'javascript/jquery.js',
            'markitup/jquery.markitup.js',
            'markitup/sets/markdown/set.js',
        )]
        css = {
            'all': [join(PAGES_MEDIA_URL, path) for path in (
                'markitup/skins/simple/style.css',
                'markitup/sets/markdown/style.css',
            )]
        }

    def render(self, name, value, attrs=None):
        rendered = super(markItUpMarkdown, self).render(name, value, attrs)
        context = {
            'name': name,
        }
        return rendered + mark_safe(render_to_string(
            'admin/pages/page/widgets/markitupmarkdown.html', context))

class markItUpHTML(Textarea):
    """markItUpHTML widget."""
    
    class Media:
        js = [join(PAGES_MEDIA_URL, path) for path in (
            'javascript/jquery.js',
            'markitup/jquery.markitup.js',
            'markitup/sets/default/set.js',
        )]
        css = {
            'all': [join(PAGES_MEDIA_URL, path) for path in (
                'markitup/skins/simple/style.css',
                'markitup/sets/default/style.css',
            )]
        }

    def render(self, name, value, attrs=None):
        rendered = super(markItUpHTML, self).render(name, value, attrs)
        context = {
            'name': name,
        }
        return rendered + mark_safe(render_to_string(
            'admin/pages/page/widgets/markituphtml.html', context))

class EditArea(Textarea):
    "EditArea is a html syntax coloured widget"
    class Media:
        js = [join(PAGES_MEDIA_URL, path) for path in (
            'edit_area/edit_area_full.js',
        )]
    
        
    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'editarea',}
        if attrs:
            self.attrs.update(attrs)
        super(EditArea, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(EditArea, self).render(name, value, attrs)
        context = {
            'name': name,
            'language': self.language,
            'PAGES_MEDIA_URL': PAGES_MEDIA_URL,
        }
        return rendered + mark_safe(render_to_string(
            'admin/pages/page/widgets/editarea.html', context))
