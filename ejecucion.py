# =====================================================================
# 4. EJECUCIÓN / INTERFAZ DE CONSOLA
# =====================================================================

if __name__ == "__main__":
    # Verificar GOOGLE_API_KEY si existe en entorno antes de correr script
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: Configurar la variable de entorno 'OPENAI_API_KEY'")
        exit(1)
        
    print("Se inicia la configuración del agente educativo...")
    documentos = cargar_y_procesar_csvs()
    
    if not documentos:
        print("No se pudieron cargar documentos. Cancelando...")
        exit(1)
        
    retriever = crear_base_conocimiento(documentos)
    agent = inicializar_agente_educativo(retriever)
    
    print("\n Agente en línea! pregunta. Escribe 'salir' para terminar.\n")
    
    while True:
        pregunta = input("Estudiante: ")
        if pregunta.lower() in ['salir', 'exit', 'quit']:
            print("Agente: ¡Hasta luego! Mucho éxito en tus estudios.")
            break
            
        if pregunta.strip() == "":
            continue
            
        # Ejecutar consulta
        respuesta = agent.invoke({"input": pregunta})
        
        print(f"\nAgente: {respuesta['answer']}")
        print("-" * 50)