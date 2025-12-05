"""
Route handlers using SQLAlchemy ORM.
Blueprint: modular route collections.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Record
from app.forms import RecordForm

# Create blueprint (like mini-application)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/records')
def list_records():
    """
    List all records.
    SQLAlchemy Query API: pythonic database queries.
    """
    # Get search query from URL parameters (?q=search_term)
    search_query = request.args.get('q', '').strip()
    
    # Build query using ORM
    query = Record.query  # Start with all records
    
    if search_query:
        # filter: adds WHERE clause
        # contains: SQL LIKE operator
        query = query.filter(Record.title.contains(search_query))
    
    # order_by: adds ORDER BY clause
    # desc(): descending order
    # all(): executes query, returns list of Record objects
    records = query.order_by(Record.created_at.desc()).all()
    
    return render_template('records_list.html', records=records, search_query=search_query)

@main_bp.route('/records/new', methods=['GET', 'POST'])
def create_record():
    """Create new record using ORM"""
    form = RecordForm()
    
    if form.validate_on_submit():
        # Create model instance
        record = Record(
            title=form.title.data,
            content=form.content.data
        )
        
        # Add to session (staging area)
        db.session.add(record)
        
        # Commit session (write to database)
        # Transactions: all-or-nothing operations
        db.session.commit()
        
        flash('Record created successfully!', 'success')
        return redirect(url_for('main.list_records'))
    
    return render_template('form.html', form=form, action='Create')

@main_bp.route('/records/<int:id>')
def view_record(id):
    """View single record"""
    # get_or_404: fetch by primary key, or return 404 error
    record = Record.query.get_or_404(id)
    return render_template('record_detail.html', record=record)

@main_bp.route('/records/<int:id>/edit', methods=['GET', 'POST'])
def edit_record(id):
    """Edit existing record"""
    record = Record.query.get_or_404(id)
    form = RecordForm()
    
    if form.validate_on_submit():
        # Update model attributes
        record.title = form.title.data
        record.content = form.content.data
        
        # Commit changes (no need to add - already tracked)
        db.session.commit()
        
        flash('Record updated successfully!', 'success')
        return redirect(url_for('main.view_record', id=record.id))
    
    # Pre-fill form with existing data
    if not form.is_submitted():
        form.title.data = record.title
        form.content.data = record.content
    
    return render_template('form.html', form=form, action='Edit', record_id=id)

@main_bp.route('/records/<int:id>/delete', methods=['POST'])
def delete_record(id):
    """Delete record"""
    record = Record.query.get_or_404(id)
    
    # Delete from session
    db.session.delete(record)
    db.session.commit()
    
    flash('Record deleted successfully!', 'success')
    return redirect(url_for('main.list_records'))
