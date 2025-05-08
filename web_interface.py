#!/usr/bin/env python3
"""
Web interface for the Prompt Management System.
This provides a simple web UI to interact with the prompt database.
"""

import os
import sys
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from prompt_manager import PromptDB, OpenRouterClient

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Check for OpenRouter API key and model
openrouter_api_key = os.environ.get('OPENROUTER_API_KEY')
openrouter_model = os.environ.get('OPENROUTER_MODEL')

if not openrouter_api_key:
    print("Error: OPENROUTER_API_KEY environment variable not set")
    sys.exit(1)

if not openrouter_model:
    print("Error: OPENROUTER_MODEL environment variable not set")
    sys.exit(1)

# Initialize the clients
db = PromptDB()
openrouter = OpenRouterClient(openrouter_api_key, openrouter_model)

@app.route('/')
def index():
    """Display the main page with a list of prompts."""
    prompts = db.get_all_prompts()
    return render_template('index.html', prompts=prompts)

@app.route('/prompt/<prompt_id>')
def view_prompt(prompt_id):
    """Display a specific prompt."""
    prompt = db.get_prompt(prompt_id)
    if not prompt:
        flash(f"Prompt with ID {prompt_id} not found")
        return redirect(url_for('index'))
    return render_template('view_prompt.html', prompt=prompt)

@app.route('/add', methods=['GET', 'POST'])
def add_prompt():
    """Add a new prompt."""
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        category = request.form.get('category')
        subcategory = request.form.get('subcategory')
        tool = request.form.get('tool')
        compatible = request.form.get('compatible')
        tags = request.form.get('tags')
        notes = request.form.get('notes')
        auto_categorize = request.form.get('auto_categorize') == 'on'
        
        prompt_data = {
            'Prompt Title': title,
            'Prompt Text': text,
            'Category': category or '',
            'Subcategory': subcategory or '',
            'Primary Tool': tool or '',
            'Compatible Tools': compatible or '',
            'Tags': tags or '',
            'Notes': notes or ''
        }
        
        # Auto-categorize if requested
        if auto_categorize:
            flash("Auto-categorizing prompt...")
            categorization = openrouter.categorize_prompt(text)
            prompt_data.update(categorization)
        
        prompt_id = db.add_prompt(prompt_data)
        
        if prompt_id:
            flash(f"Added new prompt with ID: {prompt_id}")
            return redirect(url_for('view_prompt', prompt_id=prompt_id))
        else:
            flash("Error adding prompt")
            return render_template('add_prompt.html', prompt_data=prompt_data)
    
    return render_template('add_prompt.html')

@app.route('/edit/<prompt_id>', methods=['GET', 'POST'])
def edit_prompt(prompt_id):
    """Edit an existing prompt."""
    prompt = db.get_prompt(prompt_id)
    if not prompt:
        flash(f"Prompt with ID {prompt_id} not found")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        category = request.form.get('category')
        subcategory = request.form.get('subcategory')
        tool = request.form.get('tool')
        compatible = request.form.get('compatible')
        tags = request.form.get('tags')
        notes = request.form.get('notes')
        
        prompt_data = {}
        if title:
            prompt_data['Prompt Title'] = title
        if text:
            prompt_data['Prompt Text'] = text
        if category:
            prompt_data['Category'] = category
        if subcategory:
            prompt_data['Subcategory'] = subcategory
        if tool:
            prompt_data['Primary Tool'] = tool
        if compatible:
            prompt_data['Compatible Tools'] = compatible
        if tags:
            prompt_data['Tags'] = tags
        if notes:
            prompt_data['Notes'] = notes
        
        success = db.update_prompt(prompt_id, prompt_data)
        
        if success:
            flash(f"Updated prompt with ID: {prompt_id}")
            return redirect(url_for('view_prompt', prompt_id=prompt_id))
        else:
            flash("Error updating prompt")
            return render_template('edit_prompt.html', prompt=prompt)
    
    return render_template('edit_prompt.html', prompt=prompt)

@app.route('/filter')
def filter_prompts():
    """Filter prompts based on criteria."""
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    tool = request.args.get('tool')
    tags = request.args.get('tags')
    
    filters = {}
    if category:
        filters['Category'] = category
    if subcategory:
        filters['Subcategory'] = subcategory
    if tool:
        filters['Primary Tool'] = tool
    if tags:
        filters['Tags'] = tags
    
    prompts = db.filter_prompts(filters)
    return render_template('index.html', prompts=prompts, filters=filters)

@app.route('/analyze/<prompt_id>')
def analyze_prompt(prompt_id):
    """Analyze a prompt for effectiveness."""
    prompt = db.get_prompt(prompt_id)
    if not prompt:
        flash(f"Prompt with ID {prompt_id} not found")
        return redirect(url_for('index'))
    
    flash(f"Analyzing prompt: {prompt.get('Prompt Title')}")
    analysis = openrouter.analyze_prompt_effectiveness(prompt.get('Prompt Text', ''))
    
    # Update the prompt with the analysis
    db.update_prompt(prompt_id, analysis)
    
    flash(f"Analysis complete. Rating: {analysis.get('Effectiveness Rating')}")
    return redirect(url_for('view_prompt', prompt_id=prompt_id))

@app.route('/improve/<prompt_id>', methods=['GET', 'POST'])
def improve_prompt(prompt_id):
    """Improve a prompt for a specific model."""
    prompt = db.get_prompt(prompt_id)
    if not prompt:
        flash(f"Prompt with ID {prompt_id} not found")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        target_model = request.form.get('model') or prompt.get('Primary Tool') or "general"
        
        flash(f"Improving prompt for {target_model}: {prompt.get('Prompt Title')}")
        improved_prompt = openrouter.improve_prompt(prompt.get('Prompt Text', ''), target_model)
        
        # Update the prompt with the improved version
        improved_versions = prompt.get('Improved Versions', '')
        if improved_versions:
            improved_versions += f"\n\n--- {target_model} ---\n{improved_prompt}"
        else:
            improved_versions = f"--- {target_model} ---\n{improved_prompt}"
        
        db.update_prompt(prompt_id, {'Improved Versions': improved_versions})
        
        flash(f"Improvement complete. Updated prompt in the database.")
        return redirect(url_for('view_prompt', prompt_id=prompt_id))
    
    return render_template('improve_prompt.html', prompt=prompt)

@app.route('/variations/<prompt_id>', methods=['GET', 'POST'])
def generate_variations(prompt_id):
    """Generate variations for multiple models."""
    prompt = db.get_prompt(prompt_id)
    if not prompt:
        flash(f"Prompt with ID {prompt_id} not found")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        models_text = request.form.get('models')
        models = [model.strip() for model in models_text.split(',')]
        
        flash(f"Generating variations for {len(models)} models: {prompt.get('Prompt Title')}")
        variations = openrouter.generate_variations(prompt.get('Prompt Text', ''), models)
        
        # Update the prompt with all variations
        improved_versions = prompt.get('Improved Versions', '')
        
        for model, variation in variations.items():
            if improved_versions:
                improved_versions += f"\n\n--- {model} ---\n{variation}"
            else:
                improved_versions = f"--- {model} ---\n{variation}"
        
        db.update_prompt(prompt_id, {'Improved Versions': improved_versions})
        
        flash(f"Generated variations for {len(models)} models. Updated prompt in the database.")
        return redirect(url_for('view_prompt', prompt_id=prompt_id))
    
    return render_template('generate_variations.html', prompt=prompt)

@app.route('/api/categories')
def get_categories():
    """API endpoint to get all unique categories."""
    prompts = db.get_all_prompts()
    categories = set()
    for prompt in prompts:
        category = prompt.get('Category')
        if category:
            categories.add(category)
    return jsonify(list(categories))

@app.route('/api/subcategories/<category>')
def get_subcategories(category):
    """API endpoint to get all unique subcategories for a category."""
    prompts = db.get_all_prompts()
    subcategories = set()
    for prompt in prompts:
        if prompt.get('Category') == category:
            subcategory = prompt.get('Subcategory')
            if subcategory:
                subcategories.add(subcategory)
    return jsonify(list(subcategories))

@app.route('/api/tools')
def get_tools():
    """API endpoint to get all unique tools."""
    prompts = db.get_all_prompts()
    tools = set()
    for prompt in prompts:
        tool = prompt.get('Primary Tool')
        if tool:
            tools.add(tool)
        compatible = prompt.get('Compatible Tools')
        if compatible:
            for t in compatible.split(','):
                t = t.strip()
                if t:
                    tools.add(t)
    return jsonify(list(tools))

def create_templates():
    """Create the template directory and HTML templates if they don't exist."""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create base template
    with open(os.path.join(templates_dir, 'base.html'), 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Prompt Management System{% endblock %}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding-top: 20px; }
        .flash-messages { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <header class="mb-4">
            <h1><a href="/" class="text-decoration-none">Prompt Management System</a></h1>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="container-fluid">
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav">
                            <li class="nav-item">
                                <a class="nav-link" href="/">Home</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/add">Add Prompt</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
        
        <div class="flash-messages">
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    {% for message in messages %}
                        <div class="alert alert-info">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>
        
        <main>
            {% block content %}{% endblock %}
        </main>
        
        <footer class="mt-5 pt-3 border-top text-center text-muted">
            <p>&copy; 2024 Prompt Management System</p>
        </footer>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>''')
    
    # Create other templates
    # (This would be expanded with more templates in a real implementation)

if __name__ == '__main__':
    create_templates()
    app.run(debug=True)
