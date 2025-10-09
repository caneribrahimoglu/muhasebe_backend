# app/services/service_base.py
from sqlalchemy.orm import Session

class ServiceBase:
    """
    Tüm servislerin temel sınıfı.
    Ortak bağımlılıklar burada tutulur (örneğin db, logger, config).
    """
    def __init__(self, db: Session):
        self.db = db
