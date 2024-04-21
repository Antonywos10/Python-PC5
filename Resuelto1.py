import pandas as pd
import unidecode

def clean_column_names(df):
    df.columns = [unidecode.unidecode(col).replace(' ', '_').lower() for col in df.columns]
    return df

def remove_unnecessary_columns(df):
    df = df.drop(columns=['id', 'tipomoneda'], errors='ignore')
    return df

def clean_dispositivo_legal(df):
    df['dispositivo_legal'] = df['dispositivo_legal'].str.replace(',', '', regex=True)
    return df

def convert_currency(df, exchange_rate):
    df['monto_inversion_usd'] = df['monto_inversion'] * exchange_rate
    df['monto_transferencia_usd'] = df['monto_transferencia'] * exchange_rate
    return df

def map_estado(df):
    estado_mapping = {
        'Actos Previos': 'ActosPrevios',
        'Concluido': 'Concluido',
        'Resuelto': 'Resuelto',
        'Ejecucion': 'Ejecucion'
    }
    df['estado'] = df['estado'].map(estado_mapping)
    return df

def add_estado_score(df):
    score_mapping = {
        'ActosPrevios': 1,
        'Resuelto': 0,
        'Ejecucion': 2,
        'Concluido': 3
    }
    df['estado_score'] = df['estado'].map(score_mapping)
    return df

def main():
    # Leer el archivo Excel
    df = pd.read_excel('reactiva.xlsx')

    # Procesar datos
    df = clean_column_names(df)
    df = remove_unnecessary_columns(df)
    df = clean_dispositivo_legal(df)
    
    # Suponiendo que obtenemos la tasa de cambio de alguna manera
    exchange_rate = 3.5  # Ejemplo: Tasa de cambio actual
    df = convert_currency(df, exchange_rate)
    
    df = map_estado(df)
    df = add_estado_score(df)

    # Guardar a CSV o a Excel para revisión
    df.to_csv('datos_procesados.csv', index=False)

if __name__ == '__main__':
    main()

# envio_correo.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message, from_addr, to_addr, password):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()

# Uso de la función
if __name__ == "__main__":
    send_email("Test Email", "Hello, this is a test email.", "your-email@gmail.com", "recipient-email@gmail.com", "your-password")
