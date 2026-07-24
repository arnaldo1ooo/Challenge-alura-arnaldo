# Módulo para armar un asistente inteligente con LangChain y OpenAI, 
# enfocado en consultar la base de conocimiento de una academia online.

import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# =====================================================================
# 1. LECTURA Y PARSEO DE LOS ARCHIVOS CSV
# =====================================================================
def armar_lista_documentos():
    lista_docs = []
    
    # Diccionario con la estructura y campos clave de cada archivo de datos
    mapeo_fuentes = {
        'faq_cursos_certificados.csv': {
            'texto_cols': ['Pregunta', 'Respuesta'],
            'metadata_cols': ['Categoria']
        },
        'guia_uso_plataforma.csv': {
            'texto_cols': ['Categoria', 'Problema_O_Componente', 'Solucion_O_Especificacion'],
            'metadata_cols': ['Categoria']
        },
        'politica_reembolso.csv': {
            'texto_cols': ['Seccion', 'Concepto', 'Regla_Criterio'],
            'metadata_cols': ['Seccion']
        },
        'reglamento_estudiante.csv': {
            'texto_cols': ['Seccion', 'Subcategoria', 'Regla_O_Norma', 'Detalle'],
            'metadata_cols': ['Seccion', 'Subcategoria']
        },
        'programa_becas_afiliados.csv': {
            'texto_cols': ['Tipo_Programa', 'Concepto', 'Detalles_Y_Condiciones'],
            'metadata_cols': ['Tipo_Programa']
        }
    }
    
    for nom_archivo, esquema in mapeo_fuentes.items():
        if not os.path.exists(nom_archivo):
            print(f"No se encontró el archivo: {nom_archivo}. Saltando...")
            continue
            
        print(f"Leyendo y parseando {nom_archivo}...")
        dataframe = pd.read_csv(nom_archivo)
        
        # Limpiamos los espacios en las cabeceras por las dudas
        dataframe.columns = dataframe.columns.str.strip()
        
        for _, registro in dataframe.iterrows():
            # Armamos un bloque unificado con los datos útiles para el embedding
            bloques_txt = []
            for col_actual in dataframe.columns:
                if pd.notna(registro[col_actual]):
                    bloques_txt.append(f"{col_actual}: {registro[col_actual]}")
            
            texto_unificado = "\n".join(bloques_txt)
            
            # Definimos los metadatos para filtrar luego
            meta_dict = {"fuente": nom_archivo}
            for campo_meta in esquema['metadata_cols']:
                if campo_meta in dataframe.columns and pd.notna(registro[campo_meta]):
                    meta_dict[campo_meta] = str(registro[campo_meta])
                    
            # Generamos la instancia de Document y la sumamos a la lista
            lista_docs.append(Document(page_content=texto_unificado, metadata=meta_dict))
            
        print(f"Total de fragmentos generados: {len(lista_docs)}")
    return lista_docs