import json
import os
from cryptography.fernet import Fernet
from app.classes.localization import trans  # Assuming trans is defined in localization module
from app.visualiser import show_note_table

class NotesManager:
    """NotesManager class."""
    
    def __init__(self):
        """__init__ function."""
        self.notes = {}
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def _get_input(self, prompt: str) -> str:
        """Private function to get user input with localization."""
        localized_prompt = trans(prompt)
        return input(f"{localized_prompt}: ").strip()

    def add_note(self, title=None, content=None):
        """add_note function."""
        title = title or self._get_input("Enter note title")
        content = content or self._get_input("Enter note content")
        if title in self.notes:
            return trans("Note with title '{title}' already exists.").format(title=title)
        self.notes[title] = {"content": content, "tags": []}
        return trans("Note '{title}' added successfully.").format(title=title)

    def edit_note(self, title=None):
        """edit_note function."""
        title = title or self._get_input("Enter note title to edit")
        if title not in self.notes:
            return trans("Note with title '{title}' does not exist.").format(title=title)
        new_content = self._get_input("Enter new content")
        self.notes[title]["content"] = new_content
        return trans("Note '{title}' updated successfully.").format(title=title)

    def delete_note(self, title=None):
        """delete_note function."""
        title = title or self._get_input("Enter note title to delete")
        if title not in self.notes:
            return trans("Note with title '{title}' does not exist.").format(title=title)
        
        # Get the localized confirmation prompt and format it with the title
        confirm_prompt = trans("Are you sure you want to delete note '{title}'? (yes/no)").format(title=title)
        confirm = self._get_input(confirm_prompt).lower()
        
        if confirm == "yes":
            del self.notes[title]
            return trans("Note '{title}' deleted successfully.").format(title=title)
        
        return trans("Deletion cancelled.")

    def search_notes_by_keyword(self, keyword=None):
        """search_notes_by_keyword function."""
        keyword = keyword or self._get_input("Enter keyword to search")
        results = {title: note for title, note in self.notes.items() if keyword in note["content"]}
        if results:
            return trans("Found notes {notes}").format(notes=', '.join(results.keys()))
        return trans("No notes found with the given keyword.")

    def add_tag(self, title=None, tag=None):
        """add_tag function."""
        title = title or self._get_input("Enter note title to add a tag")
        if title not in self.notes:
            return trans("Note with title '{title}' does not exist.").format(title=title)
        tag = tag or self._get_input("Enter tag to add")
        self.notes[title]["tags"].append(tag)
        return trans("Tag '{tag}' added to note '{title}'.").format(tag=tag, title=title)

    def search_notes_by_tag(self, tag=None):
        """search_notes_by_tag function."""
        tag = tag or self._get_input("Enter tag to search")
        results = {title: note for title, note in self.notes.items() if tag in note["tags"]}
        if results:
            return trans("Found notes with tag '{tag}' - {notes}").format(tag=tag, notes=', '.join(results.keys()))
        return trans("No notes found with tag '{tag}'").format(tag=tag)

    def encrypt_note(self, title=None):
        """encrypt_note function."""
        title = title or self._get_input("Enter note title to encrypt")
        if title not in self.notes:
            return trans("Note with title '{title}' does not exist.").format(title=title)
        content = self.notes[title]["content"].encode()
        encrypted_content = self.cipher_suite.encrypt(content)
        self.notes[title]["content"] = encrypted_content.decode()
        return trans("Note '{title}' encrypted successfully.").format(title=title)

    def decrypt_note(self, title=None):
        """decrypt_note function."""
        title = title or self._get_input("Enter note title to decrypt")
        if title not in self.notes:
            return trans("Note with title '{title}' does not exist.").format(title=title)
        try:
            encrypted_content = self.notes[title]["content"].encode()
            decrypted_content = self.cipher_suite.decrypt(encrypted_content).decode()
            self.notes[title]["content"] = decrypted_content
            return trans("Note '{title}' decrypted successfully.").format(title=title)
        except Exception as e:
            return trans("Failed to decrypt note '{title}': {error}").format(title=title, error=str(e))

    def import_notes(self, file_path=None):
        """import_notes function."""
        file_path = file_path or self._get_input("Enter file path to import notes from (JSON/CSV/TXT)")
        if not os.path.exists(file_path):
            return trans("File does not exist.")
        try:
            if file_path.endswith(".json"):
                with open(file_path, "r") as file:
                    imported_notes = json.load(file)
                    self.notes.update(imported_notes)
            return trans("Notes imported successfully.")
        except Exception as e:
            return trans("Failed to import notes: {error}").format(error=str(e))

    def export_notes(self, file_path=None):
        """export_notes function."""
        file_path = file_path or self._get_input("Enter file path to export notes to (JSON/CSV/TXT)")
        try:
            if file_path.endswith(".json"):
                with open(file_path, "w") as file:
                    json.dump(self.notes, file)
            return trans("Notes exported successfully.")
        except Exception as e:
            return trans("Failed to export notes: {error}").format(error=str(e))

    def save_notes(self):
        """save_notes function."""
        try:
            with open("notes_backup.txt", "w") as file:
                for title, note in self.notes.items():
                    file.write(f"{title}: {note['content']}, Tags: {', '.join(note['tags'])}\n")
            return trans("Notes saved successfully.")
        except Exception as e:
            return trans("Error saving notes: {error}").format(error=str(e))

    def backup_notes(self):
        """backup_notes function."""
        try:
            with open("notes_backup.bak", "w") as file:
                json.dump(self.notes, file)
            return trans("Backup created successfully.")
        except Exception as e:
            return trans("Error creating backup: {error}").format(error=str(e))
    
    def show_note(self, title=None):
        """Show the content of a note by title using a table format."""
        title = title or self._get_input("Enter note title to show")
        note = self.notes.get(title)
        
        if not note:
            return trans("Note with title '{title}' does not exist.").format(title=title)
        
        # Retrieve note content and tags
        content = note["content"]
        tags = note["tags"]
        
        # Draw and return the table
        return show_note_table(title, content, tags)
