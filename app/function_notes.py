import json
import os
from cryptography.fernet import Fernet

class NotesManager:
    """NotesManager class."""
    
    def __init__(self):
        """__init__ function."""
        self.notes = {}
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def add_note(self, title=None, content=None):
        """add_note function."""
        title = title or input("Enter note title: ")
        content = content or input("Enter note content: ")
        if title in self.notes:
            return f"Note with title '{title}' already exists."
        self.notes[title] = {"content": content, "tags": []}
        return f"Note '{title}' added successfully."

    def edit_note(self, title=None):
        """edit_note function."""
        title = title or input("Enter note title to edit: ")
        if title not in self.notes:
            return f"Note with title '{title}' does not exist."
        new_content = input("Enter new content: ")
        self.notes[title]["content"] = new_content
        return f"Note '{title}' updated successfully."

    def delete_note(self, title=None):
        """delete_note function."""
        title = title or input("Enter note title to delete: ")
        if title not in self.notes:
            return f"Note with title '{title}' does not exist."
        confirm = input(f"Are you sure you want to delete note '{title}'? (yes/no): ")
        if confirm.lower() == "yes":
            del self.notes[title]
            return f"Note '{title}' deleted successfully."
        return "Deletion cancelled."

    def search_notes_by_keyword(self, keyword=None):
        """search_notes_by_keyword function."""
        keyword = keyword or input("Enter keyword to search: ")
        results = {title: note for title, note in self.notes.items() if keyword in note["content"]}
        if results:
            return f"Found notes: {', '.join(results.keys())}"
        return "No notes found with the given keyword."

    def add_tag(self, title=None, tag=None):
        """add_tag function."""
        title = title or input("Enter note title to add a tag: ")
        if title not in self.notes:
            return f"Note with title '{title}' does not exist."
        tag = tag or input("Enter tag to add: ")
        self.notes[title]["tags"].append(tag)
        return f"Tag '{tag}' added to note '{title}'."

    def search_notes_by_tag(self, tag=None):
        """search_notes_by_tag function."""
        tag = tag or input("Enter tag to search: ")
        results = {title: note for title, note in self.notes.items() if tag in note["tags"]}
        if results:
            return f"Found notes with tag '{tag}': {', '.join(results.keys())}"
        return f"No notes found with tag '{tag}'."

    def encrypt_note(self, title=None):
        """encrypt_note function."""
        title = title or input("Enter note title to encrypt: ")
        if title not in self.notes:
            return f"Note with title '{title}' does not exist."
        content = self.notes[title]["content"].encode()
        encrypted_content = self.cipher_suite.encrypt(content)
        self.notes[title]["content"] = encrypted_content.decode()
        return f"Note '{title}' encrypted successfully."

    def decrypt_note(self, title=None):
        """decrypt_note function."""
        title = title or input("Enter note title to decrypt: ")
        if title not in self.notes:
            return f"Note with title '{title}' does not exist."
        try:
            encrypted_content = self.notes[title]["content"].encode()
            decrypted_content = self.cipher_suite.decrypt(encrypted_content).decode()
            self.notes[title]["content"] = decrypted_content
            return f"Note '{title}' decrypted successfully."
        except Exception as e:
            return f"Failed to decrypt note '{title}': {str(e)}"

    def import_notes(self, file_path = None):
        """import_notes function."""
        if not file_path:
            file_path = input("Enter file path to import notes from (JSON/CSV/TXT): ")
        if not os.path.exists(file_path):
            return "File does not exist."
        try:
            if file_path.endswith(".json"):
                with open(file_path, "r") as file:
                    imported_notes = json.load(file)
                    self.notes.update(imported_notes)
            # Add CSV and TXT handling here if needed
            return "Notes imported successfully."
        except Exception as e:
            return f"Failed to import notes: {str(e)}"

    def export_notes(self, file_path = None):
        """export_notes function."""
        if not file_path:
            file_path = input("Enter file path to export notes to (JSON/CSV/TXT): ")
        try:
            if file_path.endswith(".json"):
                with open(file_path, "w") as file:
                    json.dump(self.notes, file)
            # Add CSV and TXT handling here if needed
            return "Notes exported successfully."
        except Exception as e:
            return f"Failed to export notes: {str(e)}"

    def save_notes(self):
        """save_notes function."""
        try:
            with open("notes_backup.txt", "w") as file:
                for title, note in self.notes.items():
                    file.write(f"{title}: {note['content']}, Tags: {', '.join(note['tags'])}\n")
            return "Notes saved successfully."
        except Exception as e:
            return f"Error saving notes: {str(e)}"

    def backup_notes(self):
        """backup_notes function."""
        try:
            with open("notes_backup.bak", "w") as file:
                json.dump(self.notes, file)
            return "Backup created successfully."
        except Exception as e:
            return f"Error creating backup: {str(e)}"