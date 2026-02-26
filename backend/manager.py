import os
import shutil
import datetime
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError
from .db import SessionLocal, engine
from .models import File, Base
from .schemas import FileUpdate


Base.metadata.create_all(bind=engine)


class FileManager:
    def __init__(self, storage_path=None):
        self.storage_path = storage_path or os.getcwd()

    @staticmethod
    def _normalize_path(path: str) -> str:
        return Path(path).as_posix()

    def list_files(self, search: str = None):
        with SessionLocal() as session:
            query = session.query(File)
            if search:
                normalized_search = self._normalize_path(search)
                query = query.filter(File.path.contains(normalized_search))
            return [self._to_dict(f) for f in query.all()]

    def get(self, file_id: int):
        with SessionLocal() as session:
            f = session.get(File, file_id)
            return self._to_dict(f) if f else None

    def create_from_path(self, dirpath: str, filename: str):
        normalized_dirpath = self._normalize_path(dirpath)
        full_path = f"{normalized_dirpath}/{filename}"
        os_path = full_path.replace('/', os.sep)
        stats = os.stat(os_path)
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
                os_path = path.replace('/', os.sep)
                if remove_file and os.path.exists(os_path):
                    os.remove(os_path)
                return True
            except SQLAlchemyError:
                session.rollback()
                raise

    def update(self, file_id: int, update_data):
        if isinstance(update_data, dict):
            update_model = FileUpdate.from_dict(update_data)
        elif isinstance(update_data, FileUpdate):
            update_model = update_data
        else:
            raise TypeError("update_data must be dict or FileUpdate")

        with SessionLocal() as session:
            f = session.get(File, file_id)
            if not f:
                return None
            old_path = f.path
            if update_model.name:
                f.name = update_model.name
            if update_model.comment is not None:
                f.comment = update_model.comment
            if update_model.path:
                normalized_new_path = self._normalize_path(update_model.path)
                f.path = normalized_new_path
            try:
                session.add(f)
                session.commit()
                if update_model.path and old_path != f.path:
                    try:
                        old_os_path = old_path.replace('/', os.sep)
                        new_os_path = f.path.replace('/', os.sep)
                        shutil.move(old_os_path, new_os_path)
                    except Exception:
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
