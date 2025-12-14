"""
Script de migración para agregar el campo username a la tabla users
Ejecutar: python migrate_add_username.py
"""

from sqlalchemy import create_engine, text
from database import DATABASE_URL
import os

def migrate():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Verificar si la columna ya existe
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='username';
        """))
        
        if result.fetchone():
            print("✅ La columna 'username' ya existe")
            return
        
        print("📝 Agregando columna 'username' a la tabla users...")
        
        # Agregar la columna username (nullable temporalmente)
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN username VARCHAR;
        """))
        
        # Generar usernames únicos basados en email
        conn.execute(text("""
            UPDATE users 
            SET username = SPLIT_PART(email, '@', 1) || '_' || id;
        """))
        
        # Hacer la columna NOT NULL y UNIQUE
        conn.execute(text("""
            ALTER TABLE users 
            ALTER COLUMN username SET NOT NULL;
        """))
        
        conn.execute(text("""
            CREATE UNIQUE INDEX idx_users_username ON users(username);
        """))
        
        conn.commit()
        
        print("✅ Migración completada exitosamente!")
        print("📌 Los usuarios ahora tienen username generado como: email_id")

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        print("\n💡 Si la migración falla, puedes:")
        print("   1. Eliminar la base de datos y crearla de nuevo")
        print("   2. O ejecutar manualmente las consultas SQL")
