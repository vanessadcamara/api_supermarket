from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.database import SessionLocal, engine
from app.models import Category, Product, Users, Sales, ProductSales
from datetime import datetime
import random
from tqdm import tqdm  # Biblioteca para barra de progresso

fake = Faker()

# Criar sessão para inserção otimizada
SessionLocal.configure(bind=engine)
db: Session = SessionLocal()

# Parâmetros de otimização
BATCH_SIZE = 1000  # Número de registros por inserção
TOTAL_SALES = 50_000_000  # Total de vendas

def seed_categories_and_products():
    """Cria categorias e produtos no banco de dados."""
    categories = [Category(description=fake.word()) for _ in range(50)]
    db.bulk_save_objects(categories)
    db.commit()

    products = [Product(description=fake.word(), price=round(random.uniform(1.0, 100.0), 2), id_category=random.randint(1, 50)) for _ in range(1000)]
    db.bulk_save_objects(products)
    db.commit()

def seed_users():
    print("Inserting users...")
    """Cria usuários no banco de dados."""
    users = [Users(name=fake.name(), cpf=fake.unique.ssn()) for _ in tqdm(range(1_000_000), desc="Inserindo usuários", unit=" usuários")]
    db.bulk_save_objects(users)
    db.commit()

def seed_sales():
    """Cria vendas e produtos relacionados com tratamento de erros."""
    sales_batch = []
    products_sales_batch = []
    
    with tqdm(total=TOTAL_SALES, desc="Inserindo vendas", unit=" vendas") as pbar:
        for _ in range(TOTAL_SALES):
            try:
                sale = Sales(
                    id_user=random.randint(1, 1_000_000),
                    datetime=fake.date_time_between(start_date="-5y", end_date="now"),
                )
                db.add(sale)
                db.commit()  # Salva o registro da venda
                
                # Criar de 1 a 10 produtos para cada venda
                num_products = random.randint(1, 10)
                for _ in range(num_products):
                    product_sale = ProductSales(
                        id_sale=sale.id,  # ID correto gerado pelo banco
                        id_product=random.randint(1, 1000),
                    )
                    products_sales_batch.append(product_sale)
                
                # Inserir produtos em lotes
                if len(products_sales_batch) >= BATCH_SIZE:
                    db.bulk_save_objects(products_sales_batch)
                    db.commit()
                    products_sales_batch.clear()
                    pbar.update(BATCH_SIZE)
            
            except IntegrityError as e:
                print(f"Integrity error ignored: {e}")
            except SQLAlchemyError as e:
                print(f"SQLAlchemy error ignored: {e}")
            except Exception as e:
                print(f"Unexpected error ignored: {e}")

        # Inserir registros restantes
        if products_sales_batch:
            try:
                db.bulk_save_objects(products_sales_batch)
                db.commit()
            except Exception as e:
                print(f"Unexpected error ignored: {e}")
if __name__ == "__main__":
    print("Starting data seed...")
    #seed_categories_and_products()
    #seed_users()
    seed_sales()
