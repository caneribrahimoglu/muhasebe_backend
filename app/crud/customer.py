from sqlalchemy.orm import Session
from app import models, schemas
from app.crud import customer_address, customer_bank


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(
        code=customer.code,
        type=customer.type,
        institution_type=customer.institution_type,
        category=customer.category,
        title=customer.title,
        name=customer.name,
        tax_office=customer.tax_office,
        tax_number=customer.tax_number,
        tc_no=customer.tc_no,
        mersis_no=customer.mersis_no,
        kep_address=customer.kep_address,
        group1=customer.group1,
        group2=customer.group2,
        group3=customer.group3,
        group4=customer.group4,
        birth_date=customer.birth_date,
        currency=customer.currency,
        deposit_amount=customer.deposit_amount,
        open_account_limit=customer.open_account_limit,
        credit_limit=customer.credit_limit,
        account_cut_day=customer.account_cut_day,
        term_day=customer.term_day,
        grace_day=customer.grace_day,
        default_purchase_discount=customer.default_purchase_discount,
        default_sales_discount=customer.default_sales_discount,
        send_statement=customer.send_statement,
        limit_control=customer.limit_control,
        is_credit_customer=customer.is_credit_customer,
        use_pos_device=customer.use_pos_device,
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    # Alt ilişkiler
    if customer.addresses:
        for addr in customer.addresses:
            customer_address.create_customer_address(db, db_customer.id, addr)

    if customer.banks:
        for bank in customer.banks:
            customer_bank.create_customer_bank(db, db_customer.id, bank)

    db.refresh(db_customer)
    return db_customer


def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None

    for key, value in customer.model_dump(exclude_unset=True, exclude={"addresses", "banks"}).items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer
