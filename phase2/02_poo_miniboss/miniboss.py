class EspacioTrabajo:

    def __init__(self, id: int, nombre: str, capacidad: int, disponible: bool):
        self.__id = id
        self.__nombre = nombre
        self._capacidad = capacidad 
        self._disponible = disponible 

    def __repr__(self):
        return f"id: {self.get_id()} -- {self.get_nombre()}"
    
    def __eq__(self, other):
        return self.get_id() == other.get_id()
    
    def descripcion_detallada(self):
        return "información detallada del Espacio de Trabajo"
    
    def get_nombre(self):
        return self.__nombre
    
    def get_id(self):
        return self.__id
    
    def get_disponible(self):
        return self._disponible
    
    def set_disponible(self, nuevo_estado):
        self._disponible = nuevo_estado     
    

class Escritorio(EspacioTrabajo):

    def __init__(self, id, nombre, capacidad, disponible):
        super().__init__(id, nombre, capacidad, disponible)
    
    def __repr__(self):
        return super().__repr__()

    def descripcion_detallada(self): #type: ignore
        return "información detallada del Escritorio"


class SalaReuniones(EspacioTrabajo):

    def __init__(self, id, nombre, capacidad, disponible, equipamiento: list, reservable_por_hora: bool):
        super().__init__(id, nombre, capacidad, disponible)
        self.equipamiento = equipamiento #list
        self.reservable_por_hora = reservable_por_hora #bool

    def __repr__(self):
        return super().__repr__()
    
    def descripcion_detallada(self): #type: ignore
        return "información detallada de la Sala de Reuniones"


class OficinaPrivada(EspacioTrabajo):

    def __init__(self, id, nombre, capacidad, disponible,tiene_lockers, nro_piso):
        super().__init__(id, nombre, capacidad, disponible)
        self.tiene_lockers = tiene_lockers #bool
        self.nro_piso = nro_piso #int

    def __repr__(self):
        return super().__repr__()
    
    def descripcion_detallada(self): #type: ignore
        return "información detallada de la Oficina Privada"


class EspacioFactory:

    def crear_espacio(self, tipo, *args):
        if tipo == "espaciotrabajo":
            return EspacioTrabajo(*args)
        elif tipo == "escritorio":
            return Escritorio(*args)
        elif tipo == "salareuniones":
            return SalaReuniones(*args)
        elif tipo == "oficinaprivada":
            return OficinaPrivada(*args)
        else:
            raise ValueError("Tipo desconocido")


class Reserva:
    def __init__(self, usuario, espacio, fecha_inicio, fecha_fin):
        self.usuario = usuario
        self.espacio = espacio
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def __str__(self):
        return f"Reserva de {self.usuario} en {self.espacio.get_nombre()} del {self.fecha_inicio} al {self.fecha_fin}"


class AdministradorReservas():

    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def crear_reserva(self, usuario, espacio, fecha_inicio, fecha_fin):
        if not espacio.get_disponible():
            raise ValueError(f"El espacio '{espacio.get_nombre()}' no está disponible para reservas.")
        # Si está disponible, se realiza la reserva
        espacio.set_disponible(False)  # Opcional: marcar el espacio como no disponible
        return Reserva(usuario, espacio, fecha_inicio, fecha_fin)

factory = EspacioFactory()

###########################################################

sala1 = factory.crear_espacio("salareuniones",1,"sala1",10,True, ["mesa","silla"], True)
print(sala1.equipamiento) #type: ignore
admin1 = AdministradorReservas()

escritorio1 = factory.crear_espacio("escritorio",2,"escritorio1",5,True)
escritorio1.set_disponible(False)
print(admin1.crear_reserva(
    "Ana", 
    sala1, 
    "2025-08-05", 
    "2025-08-05"
))
print(sala1)
print(escritorio1.get_disponible())
print(sala1 == escritorio1)