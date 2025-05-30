from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, abort, jsonify, flash
)
from app.models import HtmlSnippet
from app.cache import get_cached_snippet, cache_snippet

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    """Home page - form for creating new HTML snippets"""
    return render_template('index.html')

@main.route('/create', methods=['POST'])
def create_snippet():
    """Create a new HTML snippet"""
    html_content = request.form.get('html_content', '')
    
    if not html_content:
        flash('HTML content is required', 'error')
        return redirect(url_for('main.index'))
    
    # Create new snippet
    snippet = HtmlSnippet.create_snippet(
        html_content=html_content
    )
    
    # Cache the snippet
    cache_snippet(snippet)
    
    return redirect(url_for('main.view_snippet', snippet_id=snippet.id))

@main.route('/view/<snippet_id>', methods=['GET'])
def view_snippet(snippet_id):
    """View a shared HTML snippet"""
    # Try to get from cache first
    snippet_data = get_cached_snippet(snippet_id)
    
    if not snippet_data:
        # If not in cache, get from database
        snippet = HtmlSnippet.get_by_id_str(snippet_id)
        if not snippet:
            abort(404)
        
        # Cache for future requests
        snippet_data = cache_snippet(snippet)
    
    return render_template(
        'view.html',
        snippet=snippet_data
    )

@main.route('/r/<snippet_id>', methods=['GET'])
def raw_snippet(snippet_id):
    """View raw HTML content"""
    # Try to get from cache first
    snippet_data = get_cached_snippet(snippet_id)
    
    if not snippet_data:
        # If not in cache, get from database
        snippet = HtmlSnippet.get_by_id_str(snippet_id)
        if not snippet:
            abort(404)
        
        # Cache for future requests
        snippet_data = cache_snippet(snippet)
    
    return snippet_data['html_content']

@main.route('/preview/<snippet_id>', methods=['GET'])
def preview_snippet(snippet_id):
    """Preview HTML content in an iframe-friendly page"""
    # Try to get from cache first
    snippet_data = get_cached_snippet(snippet_id)
    
    if not snippet_data:
        # If not in cache, get from database
        snippet = HtmlSnippet.get_by_id_str(snippet_id)
        if not snippet:
            abort(404)
        
        # Cache for future requests
        snippet_data = cache_snippet(snippet)
    
    return render_template(
        'preview.html',
        snippet=snippet_data
    )
