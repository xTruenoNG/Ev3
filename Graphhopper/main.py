import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "bd143625-fedb-4612-a4ae-261540d815ae"

def geocodificacion(location, clave):
    while location == "":
        location = input("Ingresa la ubicación nuevamente: ")
    url_geocodificacion = "https://graphhopper.com/api/1/geocode?"
    url = url_geocodificacion + urllib.parse.urlencode({"q": location, "limit": "1", "key": clave})

    respuesta_datos = requests.get(url)
    datos_json = respuesta_datos.json()
    estado_json = respuesta_datos.status_code

    if estado_json == 200:
        datos_json = requests.get(url).json()
        latitud = datos_json["hits"][0]["point"]["lat"]
        longitud = datos_json["hits"][0]["point"]["lng"]
        nombre = datos_json["hits"][0]["name"]
        valor = datos_json["hits"][0]["osm_value"]

        if "country" in datos_json["hits"][0]:
            pais = datos_json["hits"][0]["country"]
        else:
            pais = ""

        if "state" in datos_json["hits"][0]:
            estado = datos_json["hits"][0]["state"]
        else:
            estado = ""

        if len(estado) != 0 and len(pais) != 0:
            nueva_ubicacion = nombre + ", " + estado + ", " + pais
        elif len(estado) != 0:
            nueva_ubicacion = nombre + ", " + pais
        else:
            nueva_ubicacion = nombre

        print("URL de la API de geocodificación para " + nueva_ubicacion + " (Tipo de ubicación: " + valor + ")\n" + url)
    else:
        latitud = "null"
        longitud = "null"
        nueva_ubicacion = location
    return estado_json, latitud, longitud, nueva_ubicacion

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("coche, bicicleta, a pie")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    perfiles = ["coche", "bicicleta", "a pie"]
    vehiculo = input("Ingresa un perfil de vehículo de la lista anterior: ")
    if vehiculo == "salir" or vehiculo == "q":
        break
    elif vehiculo in perfiles:
        vehiculo = vehiculo
    else:
        vehiculo = "coche"
        print("No se ingresó un perfil de vehículo válido. Se utilizará el perfil de coche.")
    loc1 = input("Ubicación de inicio: ")
    if loc1 == "salir" or loc1 == "q":
        break
    orig = geocodificacion(loc1, key)
    loc2 = input("Destino: ")
    if loc2 == "salir" or loc2 == "q":
        break
    dest = geocodificacion(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehiculo": vehiculo}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de enrutamiento: " + str(paths_status) + "\nURL de la API de enrutamiento:\n" + paths_url)
        print("=================================================")
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3] + " en " + vehiculo)
        print("=================================================")
        if paths_status == 200:
            km = (paths_data["paths"][0]["distance"]) / 1000
            seg = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia recorrida: {0:.1f} km".format(km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, seg))
            print("=============================================")
            for cada in range(len(paths_data["paths"][0]["instructions"])):
                instruccion = paths_data["paths"][0]["instructions"][cada]["text"]
                distancia = paths_data["paths"][0]["instructions"][cada]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} millas )".format(instruccion, distancia/1000, distancia/1000/1.61))
                print("=============================================")
        else:
            print("Mensaje de error: " + paths_data["message"])
            print("*************************************************")
