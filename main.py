from pathlib import Path
import datetime

from data.database_yoneticisi import DatabaseManager
from data.veri_olusturma import DataGenerator
from sorgular import fetch_sales_by_month,fetch_sales_by_product,fetch_top_customers

def setup_database():
    create_sales_table = '''CREATE TABLE IF NOT EXISTS sales (
                                sale_id INTEGER PRIMARY KEY,
                                sale_date DATE,
                                customer_id INTEGER,
                                product_id INTEGER,
                                quantity INTEGER,
                                unit_price DECIMAL(10, 2),
                                total_price DECIMAL(10, 2),
                                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                                FOREIGN KEY (product_id) REFERENCES products(product_id)
                             )'''

    create_products_table = '''CREATE TABLE IF NOT EXISTS products (
                                product_id INTEGER PRIMARY KEY,
                                product_name TEXT,
                                unit_cost DECIMAL(10, 2)
                             )'''

    create_customers_table = '''CREATE TABLE IF NOT EXISTS customers (
                                customer_id INTEGER PRIMARY KEY,
                                first_name TEXT,
                                last_name TEXT,
                                email TEXT,
                                phone TEXT
                             )'''

    # Sample data
    products = [
        ('Telefon', 50.00), 
        ('Bilgisayar', 25.00), 
        ('Klavye', 75.00), 
        ('Kumanda', 40.00), 
        ('Televizyon', 60.00)
    ]
    customers = [
        ('John', 'Doe', 'johndoe@example.com', '555-1234'),
        ('Jane', 'Doe', 'janedoe@example.com', '555-5678'),
        ('Bob', 'Smith', 'bobsmith@example.com', '555-9012'),
        ('Alice', 'Jones', 'alicejones@example.com', '555-3456'),
        ('David', 'Brown', 'davidbrown@example.com', '555-7890'),
        ('Emily', 'Davis', 'emilydavis@example.com', '555-2345'),
        ('Frank', 'Wilson', 'frankwilson@example.com', '555-6789'),
        ('Grace', 'Lee', 'gracelee@example.com', '555-1234'),
        ('Henry', 'Chen', 'henrychen@example.com', '555-5678'),
        ('Isabel', 'Garcia', 'isabelgarcia@example.com', '555-9012')
    ]

    # Initialize the database manager
    db_manager = DatabaseManager('sales.db')
    
    # Create tables
    db_manager.create_table(create_sales_table)
    db_manager.create_table(create_products_table)
    db_manager.create_table(create_customers_table)


    # VEri Ekleme İşlemleri
    db_manager.insert_data('INSERT INTO products (product_name, unit_cost) VALUES (?,?)',products)
    db_manager.insert_data('INSERT INTO customers (first_name, last_name, email, phone) VALUES (?,?,?,?)',customers)

    # Müşteriler ve aldıkları ürünlerin ID lerdinden Satışlar tablosuna veri ekleyeceğim
    start_date = datetime.date(2023,1,1)
    end_date =   datetime.date(2024,8,25)
    data_generator = DataGenerator(start_date,end_date)
    sales_data = data_generator.generate_sales_data(customers,products,200)
    db_manager.insert_data('''INSERT INTO sales (sale_date, customer_id, product_id, quantity, unit_price, total_price) VALUES (?,?,?,?,?,?)''',sales_data)

    db_manager.commit()
    db_manager.close()



from database import connect_db
def generate_query():
    connection = connect_db()
    aylik_satislar_df = fetch_sales_by_month(connection)
    urun_satislar_df = fetch_sales_by_product(connection)
    en_iyi_musteriler = fetch_top_customers(connection)
    print(f""" -------------------------------------
                AYLIK SATIŞLAR
                {aylik_satislar_df}
            -------------------------------------------
                URUNLERİN SATISLARI
                {urun_satislar_df}
            --------------------------------------------
                EN İYİ MUSTERİLER
            --------------------------------------------
                {en_iyi_musteriler}
            -------------------------------------------
            """)
    

from grafikler.aylik_satislar_grafigi import aylik_satis_grafigi_olusturma
from grafikler.musteri_satislari_graifkleri import musteri_satis_grafigi
from grafikler.urun_satislar_grafigi import urunler_satis_grafigi
from grafikler.pdf_report import create_pdf_report

def grafik_olustur(output_dir):
    connection = connect_db()
    aylik_satislar_df = fetch_sales_by_month(connection)
    urun_satislar_df = fetch_sales_by_product(connection)
    en_iyi_musteriler = fetch_top_customers(connection)

    aylik_satis_grafigi_olusturma(aylik_satislar_df,output_dir)
    musteri_satis_grafigi(en_iyi_musteriler, output_dir)
    urunler_satis_grafigi(urun_satislar_df, output_dir)

    connection.close()

if __name__ == '__main__':
    output_dir = Path('output')
    #output_dir.mkdir(exist_ok=True)
    grafik_olustur(output_dir)
    create_pdf_report(output_dir)

    # setup_database()
    generate_query()