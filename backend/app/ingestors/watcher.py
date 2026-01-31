import time
import os
import shutil
import uuid
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.core.config import settings
from app.ingestors.text_extract import extract_text_from_file
from app.db.store import add_file
from app.core.embeddings import embed_and_store

class IngestHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        self.process(event.src_path)

    def process(self, src_path):
        # basic flow: move to storage, extract, embed, save metadata
        os.makedirs(settings.storage_dir, exist_ok=True)
        fname = os.path.basename(src_path)
        new_id = str(uuid.uuid4())
        dest = os.path.join(settings.storage_dir, f"{new_id}_{fname}")
        try:
            shutil.move(src_path, dest)
        except Exception:
            # if can't move (maybe same fs), copy
            shutil.copy(src_path, dest)
        text = extract_text_from_file(dest)
        snippet = (text[:500] + "...") if len(text) > 500 else text
        meta = {"id": new_id, "filename": fname, "path": dest, "content_snippet": snippet}
        # store JSON metadata
        add_file(meta)
        # generate embedding and add to FAISS
        embed_and_store(new_id, text)

def start_watcher():
    os.makedirs(settings.ingest_dir, exist_ok=True)
    event_handler = IngestHandler()
    observer = Observer()
    observer.schedule(event_handler, path=settings.ingest_dir, recursive=False)
    observer.start()
    print(f"Watching {settings.ingest_dir} for new files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
