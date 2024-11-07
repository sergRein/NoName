class NotesManager:
    def __init__(self):
        self.notes = {}

    def add_note(self, title, content):
        if title in self.notes:
            return f"Note with title '{title}' already exists."
        self.notes[title] = content
        return f"Note '{title}' added successfully."

    def edit_note(self, title, new_content):
        if title not in self.notes:
            return f"Note with title '{title}' does not exist."
        self.notes[title] = new_content
        return f"Note '{title}' updated successfully."

    def save_notes(self):
        # Example: saving notes to a file (can be expanded as needed)
        try:
            with open("notes_backup.txt", "w") as file:
                for title, content in self.notes.items():
                    file.write(f"{title}: {content}\n")
            return "Notes saved successfully."
        except Exception as e:
            return f"Error saving notes: {str(e)}"
