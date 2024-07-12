import numpy as np

# Definir las tasas de llegada y servicio según los parámetros
tasa_llegada_retiro = {
    'rápido': 1/1,
    'normal': 1/2,
    'lento': 1/3,
    'muy lento': 1/3
}

tasa_servicio_retiro = {
    'rápido': 1/1,
    'normal': 1/2,
    'lento': 1/3,
    'muy lento': 1/4
}

tasa_llegada_pago = {
    'rápido': 1/1,
    'normal': 1/2,
    'lento': 1/3,
    'muy lento': 1/4
}

tasa_servicio_pago = {
    'rápido': 1/3,
    'normal': 1/3,
    'lento': 1/5,
    'muy lento': 1/7
}

# Probabilidades de tipos de usuario
prob_retiro = [0.23, 0.40, 0.17, 0.20]
prob_pago = [0.10, 0.20, 0.30, 0.40]

# Tipos de usuario
tipos_de_usuario = ['rápido', 'normal', 'lento', 'muy lento']

# Simular un día de operaciones en el banco
def simulate_day():
    total_usarios = 0
    tiempos_espera = []
    contar_usuarios = {ut: 0 for ut in tipos_de_usuario}
    
    for _ in range(3):  # Tres cajeros
        tiempo = 0
        queue = []
        while tiempo < 8 * 60:  # 8 horas de operación
            # Decidir si es retiro o pago
            if np.random.rand() >= 0.3:
                tipo_accion = 'retiro'
                tasa_llegada = np.random.choice(list(tasa_llegada_retiro.values()), p=prob_retiro)
                tasa_servicio = np.random.choice(list(tasa_servicio_retiro.values()), p=prob_retiro)
            else:
                tipo_accion = 'pago'
                tasa_llegada = np.random.choice(list(tasa_llegada_pago.values()), p=prob_pago)
                tasa_servicio = np.random.choice(list(tasa_servicio_pago.values()), p=prob_pago)

            
            # Tiempo hasta la próxima llegada
            interarrival_time = np.random.exponential(scale=1/tasa_llegada)
            tiempo += interarrival_time
            if tiempo >= 8 * 60:
                break
            
            # Tipo de usuario
            tipo_usr = np.random.choice(tipos_de_usuario, p=prob_retiro if tipo_accion == 'retiro' else prob_pago)
            contar_usuarios[tipo_usr] += 1
            
            # Tiempo de servicio
            tiempo_servicio = np.random.exponential(scale=1/tasa_servicio)
            if queue:
                queue[-1][1] += tiempo_servicio  # Agregar el tiempo de servicio al último usuario en la cola
            queue.append([tiempo, tiempo_servicio])
            total_usarios += 1

        
        
        # Calcular tiempos de espera
        tiempo_inicio_servicio = 0
        for tiempo_llegada, tiempo_servicio in queue:
            if tiempo_inicio_servicio < tiempo_llegada:
                tiempo_inicio_servicio = tiempo_llegada
            tiempo_de_espera = tiempo_inicio_servicio - tiempo_llegada + tiempo_servicio
            tiempos_espera.append(tiempo_de_espera)
            tiempo_inicio_servicio += tiempo_servicio
    
        print(
            f"Tipo de accion:" , tipo_accion.swapcase(), 
            "\n\tTiempo de Servicio:" , tiempo_servicio , 
            "\n\t\t Usuario Atendido en caja" , _ + 1 , "\n"            
            )

    promedio_tiempo_espera = np.mean(tiempos_espera)
    return promedio_tiempo_espera, contar_usuarios, total_usarios

# Realizar múltiples corridas
def simulacion_banco(num_simulaciones):
    results = []
    for _ in range(num_simulaciones):
        results.append(simulate_day())
    return results

# Ejecutar la simulación
simulaciones = 10
result = simulacion_banco(simulaciones)

# Calcular estadísticas
promedio_esperas = [r[0] for r in result]
conteo_usuarios_general = [r[1] for r in result]
total_usuarios_general = [r[2] for r in result]

promedio_espera_general = np.mean(promedio_esperas)
promedio_usuarios = {ut: np.mean([user_counts[ut] for user_counts in conteo_usuarios_general]) for ut in tipos_de_usuario}

print("\nTiempo promedio de espera:", promedio_espera_general , "\n")
print("Promedio de usuarios de cada tipo:", promedio_usuarios , "\n")


""" Total del usuarios en Lista y en cascada """

print("Total de usuarios en todas las corridas:", total_usuarios_general , "\n")

for idx, usuarios in enumerate(total_usuarios_general, start=1):
    print(f"El Total de usuarios en corrida" , idx , "es:" , usuarios)


