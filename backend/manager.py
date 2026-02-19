import os
import shutil
import datetime
from sqlalchemy.exc import SQLAlchemyError
from .db import SessionLocal, engine
from .models import File, Base


Base.metadata.create_all(bind=engine)


class FileManager:
    def __init__(self, storage_path=None):
        self.storage_path = storage_path or os.getcwd()

    def list_files(self, search: str = None):
        with SessionLocal() as session:
            query = session.query(File)
            if search:
                query = query.filter(File.path.contains(search))
            return [self._to_dict(f) for f in query.all()]

    def get(self, file_id: int):
        with SessionLocal() as session:
            f = session.get(File, file_id)
            return self._to_dict(f) if f else None

    def create_from_path(self, dirpath: str, filename: str):
        full_path = os.path.join(dirpath, filename)
        stats = os.stat(full_path)
        name, extension = os.path.splitext(filename)
        extension = extension.lstrip('.')
        file_obj = File(
            name=name,
            extension=extension,
            size=stats.st_size,
            path=full_path,
            created_at=datetime.datetime.fromtimestamp(stats.st_ctime),
            updated_at=datetime.datetime.fromtimestamp(stats.st_mtime),
        )
        with SessionLocal() as session:
            try:
                session.add(file_obj)
                session.commit()
                session.refresh(file_obj)
                return self._to_dict(file_obj)
            except SQLAlchemyError:
                session.rollback()
                raise

    def delete(self, file_id: int, remove_file: bool = True):
        with SessionLocal() as session:
            f = session.get(File, file_id)
            if not f:
                return False
            path = f.path
            try:
                session.delete(f)
                session.commit()
                if remove_file and os.path.exists(path):
                    os.remove(path)
                return True
            except SQLAlchemyError:
                session.rollback()
                raise

    def update(self, file_id: int, name: str = None, new_path: str = None, comment: str = None):
        with SessionLocal() as session:
            f = session.get(File, file_id)
            if not f:
                return None
            old_path = f.path
            if name:
                f.name = name
            if comment is not None:
                f.comment = comment
            if new_path:
                f.path = new_path
            try:
                session.add(f)
                session.commit()
                # Try moving file on filesystem; if fails, rollback DB change
                if new_path and old_path != new_path:
                    try:
                        shutil.move(old_path, new_path)
                    except Exception as e:
                        session.rollback()
                        raise
                session.refresh(f)
                return self._to_dict(f)
            except SQLAlchemyError:
                session.rollback()
                raise

    def _to_dict(self, f: File):
        if not f:
            return None
        return {
            'id': f.id,
            'name': f.name,
            'extension': f.extension,
            'size': f.size,
            'path': f.path,
            'created_at': f.created_at.isoformat() if f.created_at else None,
            'updated_at': f.updated_at.isoformat() if f.updated_at else None,
            'comment': f.comment,
        }
