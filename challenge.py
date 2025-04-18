"""
Este script procesa un archivo CSV con información de contactos y calcula
un puntaje para cada uno basado en tres criterios: rol, tamaño de la empresa y país.

El puntaje final se calcula asignando distintos pesos a cada criterio, considerando
como más importante el rol del contacto, seguido por el tamaño de la empresa y por último el país.
Luego, los contactos se ordenan de mayor a menor puntaje, priorizando aquellos con mayor relevancia para ventas.

El resultado se guarda en un nuevo archivo CSV para su posterior análisis.

Criterios utilizados:
- Rol: Se asignan puntajes según el poder de decisión estimado del cargo.
- Tamaño de la empresa: Las empresas más grandes reciben mayor puntaje.
- País: Se asigna puntaje según los niveles de importancia definidos por tiers (niveles).

Requisitos:
- El archivo 'data.csv' debe estar ubicado en el mismo directorio que este script.
- El resultado se guarda como 'contact_plan.csv' en el mismo directorio.

Dependencias:
- pandas (para manipulación de datos)

Cómo ejecutar:
    $ python challenge.py
"""

import pandas as pd
import os

# Mapeos para los puntajes de los distintos criterios.
ROLE_SCORES = {
    'ceo': 100,
    'cfo': 90,
    'cto': 90,
    'manager': 80,
    'consultant': 70,
    'engineer': 60,
    'developer': 50,
    'analyst': 40,
    'designer': 30,
    'intern': 10
}

COMPANY_SIZE_SCORES = {
    '10000+': 100,
    '5001-10000': 90,
    '1001-5000': 80,
    '501-1000': 70,
    '201-500': 60,
    '51-200': 50,
    '11-50': 30,
    '1-10': 20
}

COUNTRY_TIERS = {
    'tier_1': {
        'usa', 'uk', 'germany', 'france', 'canada', 'australia'
    },
    'tier_2': {
        'spain', 'italy', 'brazil', 'india'
    }
}

COUNTRY_SCORES = {
    'tier_1': 100,
    'tier_2': 80,
    'other': 60 # Si no está en ninguno de los tiers anteriores, se asigna este puntaje.
}

def assign_role_score(role):
    """ Asigna un puntaje basado en el rol del contacto. """
    role = role.lower()
    return ROLE_SCORES.get(role, 20)  # Si no existe el rol, retorna 20.

def assign_company_size_score(size):
    """ Asigna un puntaje basado en el tamaño de la empresa. """
    return COMPANY_SIZE_SCORES.get(size, 20)  # 20 en este caso es también el valor por defecto que le doy.

def assign_country_score(country):
    """ Asigna un puntaje basado en el país. """
    country = country.lower()
    if country in COUNTRY_TIERS['tier_1']:
        return COUNTRY_SCORES['tier_1']
    elif country in COUNTRY_TIERS['tier_2']:
        return COUNTRY_SCORES['tier_2']
    return COUNTRY_SCORES['other']

def process_contacts():
    """ Procesa el archivo CSV de contactos y los ordena según relevancia para ventas. """
    # Acá se definen los pesos para cada criterio. En este caso tomé como más importante el rol, luego el tamaño de la empresa y por último el país.
    WEIGHTS = {
        'role': 0.5,
        'company_size': 0.3,
        'country': 0.2
    }

    # Obtener la ruta absoluta del archivo donde está el script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'data.csv')
    output_file = os.path.join(script_dir, 'contact_plan.csv')

    # Leer el archivo CSV con los datos.
    df = pd.read_csv(input_file)

    # Manejar valores nulos. En este caso les asigno valores por defecto.
    df['Role'].fillna('unknown', inplace=True)
    df['Company Size'].fillna('1-10', inplace=True)
    df['Country'].fillna('unknown', inplace=True)

    # Calcular los puntajes
    df['role_score'] = df['Role'].apply(assign_role_score)
    df['company_size_score'] = df['Company Size'].apply(assign_company_size_score)
    df['country_score'] = df['Country'].apply(assign_country_score)

    # Calcular el puntaje final usando los pesos que se definieron antes.
    df['final_score'] = (
        df['role_score'] * WEIGHTS['role'] +
        df['company_size_score'] * WEIGHTS['company_size'] +
        df['country_score'] * WEIGHTS['country']
    )

    # Ordenar por puntaje final de mayor a menor.
    df_sorted = df.sort_values('final_score', ascending=False)

    # Eliminar las columnas de los puntajes, ya que no son necesarias.
    score_columns = ['role_score', 'company_size_score', 'country_score', 'final_score']
    df_sorted = df_sorted.drop(columns=score_columns)

    # Guardar el resultado en el nuevo archivo CSV.
    df_sorted.to_csv(output_file, index=False)

    print(f"El archivo CSV con los datos fue procesado correctamente. Los resultados fueron guardados en {output_file}.")

if __name__ == '__main__':
    process_contacts()