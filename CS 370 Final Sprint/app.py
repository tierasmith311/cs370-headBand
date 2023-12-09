from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

notes = []

@app.route('/')
def index():
    load_notes()  # Load notes from file
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    # Get the note details from the form submission
    note_title = request.form['note_title']
    note_content = request.form['note_content']
    note_category = request.form.get('note_category', '')  # Optional category
    note_color = request.form['note_color']
    
    # Add the note to the list of notes
    notes.append({
        'title': note_title,
        'content': note_content,
        'category': note_category,
        'color': note_color
    })

    save_notes()  # Save notes to file
    return redirect('/')

@app.route('/delete_or_edit_note/<int:note_id>', methods=['POST'])
def delete_or_edit_note(note_id):
    action = request.form['action']

    if action == 'delete':
        # Delete the note with the given ID from the list of notes
        del notes[note_id]
        save_notes()  # Save notes to file

    elif action == 'edit':
        # Redirect to the edit page with the note ID
        return redirect(f'/edit_note/{note_id}')

    # Return the updated index page
    return redirect('/')

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if request.method == 'GET':
        # Display the edit page with the existing note details
        load_notes()  # Load notes from file
        note = notes[note_id]
        return render_template('edit_note.html', note=note, note_id=note_id)

    elif request.method == 'POST':
        # Update the note with the new details
        notes[note_id]['title'] = request.form['note_title']
        notes[note_id]['content'] = request.form['note_content']
        notes[note_id]['category'] = request.form['note_category']
        notes[note_id]['color'] = request.form['note_color']

        save_notes()  # Save notes to file
        return redirect('/')

def load_notes():
    global notes
    try:
        with open('notes.json', 'r') as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []

def save_notes():
    with open('notes.json', 'w') as file:
        json.dump(notes, file, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
