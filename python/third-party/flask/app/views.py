from flask import redirect, render_template, url_for

from . import app


@app.route('/')
def index():
    return render_template('base.htm')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.htm'), 404

"""
@blog.route("/")
def index():
    posts = (p for p in flatpages if 'published' in p.meta)
    print tags()
    latest = sorted(posts, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('blog/index.htm', posts=latest[:10])


@blog.route('/<name>/')
def page(path):
    page = flatpages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    return render_template(template, page=page)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)
"""
