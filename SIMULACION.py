'''
JAVIER ALEJANDRO PRADO RAMIREZ-21486
ALGORITMOS Y ESTRUCTURA DE DATOS
CATEDRATICO: MOISES ANTONIO ALONSO GONZALEZ
AUXILIARES: CRISTIAN FERNANDO LAYNEZ BACHEZ Y RUDIK ROBERTO ROMPICH COTZOJAY
HOJA DE TRABAJO #5: SimulaciOn de corrida de programas en un sistema operativo de tiempo compartido
'''
import simpy
import random

def proceso(nombre, env, memoria, cpu, llegada, cantidad_instrucciones, cantidad_ram):

    # Simula la espera de llegada del proceso
    yield env.timeout(llegada)

    #grabo el tiempo de llegada
    tiempo_llegada = env.now

    #PROCESO NEW
    print('%s proceso en cola [NEW llegada] -> %d cantidad ram requerida %d, disponible %d' % (nombre, env.now, cantidad_ram, memoria.level))
    yield memoria.get(cantidad_ram)  #Pide la memoria que necesita o espera automaticamente hasta que haya suficiente

    #PROCESO READY
    while cantidad_instrucciones > 0:  #repite hasta que se acabe la cantidad de instrucciones pendientes
        # Ya tiene memoria para iniciar
        print('%s proceso en cola READY tiempo -> %d cantidad instrucciones pendientes %d' % (nombre, env.now, cantidad_instrucciones))

        #PROCESO RUNNING
        with cpu.request() as req:  #pide el procesador
            yield req

            cantidad_instrucciones = cantidad_instrucciones - 3
            yield env.timeout(1) #Simula un ciclo de reloj del procesador

            # Ya tiene procesador
            print('%s proceso en estado RUNNING fue atendido en tiempo -> %d cantidad ram %d, Instrucciones pendientes %d ram disponible %d' % (nombre, env.now, cantidad_ram, cantidad_instrucciones, memoria.level))
            if  cantidad_instrucciones > 0:
                numeroRandom = random.randint(1, 2)
                if numeroRandom == 1:
                    yield env.timeout(1)
                    print('%s proceso en estado WAITING(haciendo operaciones de I/O..) fue atendido en tiempo -> %d cantidad ram %d, Instrucciones pendientes %d ram disponible %d' % (nombre, env.now, cantidad_ram, cantidad_instrucciones, memoria.level))
            else:
                # Cuando ya finaliza devuelve la memoria utilizada
                yield memoria.put(cantidad_ram)

                #PROCESO TERMINATED
                print('%s proceso TERMINATED salida -> %d cantidad ram devuelta %d, nueva cantidad de memoria disponible %d' % (nombre, env.now, cantidad_ram, memoria.level))
                global tiempo_total
                tiempo_total += env.now - tiempo_llegada
                print('Tiempo total %d' % (env.now - tiempo_llegada))
                

    


random.seed(10)
env = simpy.Environment()  # crear ambiente de simulacion
initial_ram = simpy.Container(env, 100, init=100)  # crea el container de la ram
initial_cpu = simpy.Resource(env, capacity=1)  # se crea el procesador con capacidad establecida
initial_procesos = 25 # cantidad de procesos a generar
INTERVAL = 1 #modificara la velocidad en hacer tareas IMPORTANTE
intervalINSTRUCTIONS = [1, 10]
intervalRAM = [1, 10]
tiempo_total = 0



def SOURCE(env, initial_procesos, INTERVAL, initial_ram,initial_cpu,  intervalINSTRUCTIONS, intervalRAM):
    for i in range(initial_procesos):
        llegada = 0 #Todos los procesos llegan al mismo tiempo
        cantidad_instrucciones = random.randint(1, 10)  # cantidad de operaciones por proceso
        UsoRam = random.randint(1, 10)  # cantidad de ram que requiere cada proceso
        env.process(proceso('proceso %d' % i, env, initial_ram, initial_cpu, llegada, cantidad_instrucciones, UsoRam))
        #para que sea exponencial
        t = random.expovariate(1.0 / INTERVAL)
        yield env.timeout(t)


# correr la simulacion
env.process(SOURCE(env, initial_procesos, INTERVAL, initial_ram,initial_cpu,  intervalINSTRUCTIONS, intervalRAM))
env.run()
print('tiempo promedio %d ' % (tiempo_total / initial_procesos))