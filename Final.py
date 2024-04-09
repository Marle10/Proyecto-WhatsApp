import threading
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

class Usuario:
    def __init__(self):
        self.disponible = True

    def cambiar_disponibilidad(self, disponible):
        self.disponible = disponible

class SistemaRespuestaAutomatica:
    def __init__(self, usuario):
        self.usuario = usuario
        self.mensaje_predeterminado = "Lo siento, estoy ocupado en este momento."
        self.ultimo_estado = None
        self.mostrar_menu_configuracion = True
        self.evento_cambio_disponibilidad = threading.Event()
        self.monitor_cambio_disponibilidad = threading.Condition()

    def monitorear_estado(self):
        while True:
            with self.monitor_cambio_disponibilidad:
                while self.usuario.disponible == self.ultimo_estado:
                    self.monitor_cambio_disponibilidad.wait()
                self.ultimo_estado = self.usuario.disponible
                if not self.usuario.disponible:
                    print("Llamada no tomada. Enviando mensaje de no disponibilidad:", self.mensaje_predeterminado)
                    self.mostrar_menu_configuracion = False
                    # Llamar al método para volver a verificar el estado después de 15 segundos
                    threading.Timer(15, self.verificar_disponibilidad).start()

    def verificar_disponibilidad(self):
        # Volver a verificar el estado de disponibilidad después de 15 segundos
        if not self.usuario.disponible:
            print("Volver a verificar la disponibilidad después de 15 segundos...")
            time.sleep(15)
            if not self.usuario.disponible:
                print("Usuario todavía no disponible. Enviando mensaje de no disponibilidad nuevamente:", self.mensaje_predeterminado)
                threading.Timer(15, self.verificar_disponibilidad).start()

    async def proceso_asincrono(self):
        while True:
            await asyncio.sleep(1)
            if self.mostrar_menu_configuracion:
                # Mostrar el menú de configuración si se debe mostrar
                print("\nCONFIGURACIÓN:")
                print("1. Cambiar mensaje predeterminado")
                print("2. Cambiar preferencia de disponibilidad (disponible/no disponible)")
                print("3. Salir")
                opcion = input("Seleccione una opción: ")
                if opcion == '1':
                    nuevo_mensaje = input("Ingrese el nuevo mensaje predeterminado: ")
                    self.mensaje_predeterminado = nuevo_mensaje
                    print("Mensaje predeterminado actualizado.")
                elif opcion == '2':
                    nueva_disponibilidad = input("Seleccione la nueva preferencia de disponibilidad (1 para disponible, 0 para no disponible): ")
                    self.usuario.cambiar_disponibilidad(bool(int(nueva_disponibilidad)))
                    estado = "disponible" if self.usuario.disponible else "no disponible"
                    print(f"El usuario ahora está {estado}.")
                elif opcion == '3':
                    print("Saliendo del programa...")
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")

def main():
    usuario = Usuario()
    sistema_respuesta_automatica = SistemaRespuestaAutomatica(usuario)

    # Iniciar hilo de monitoreo del estado de ocupación
    hilo_monitoreo = threading.Thread(target=sistema_respuesta_automatica.monitorear_estado)
    hilo_monitoreo.start()

    # Ejecutar proceso asincrónico con asyncio
    asyncio.run(sistema_respuesta_automatica.proceso_asincrono())

if __name__ == "__main__":
    main()
