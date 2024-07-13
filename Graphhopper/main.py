import requests
import urllib.parse
import folium

route_url = "https://graphhopper.com/api/1/route?"
key = "bd143625-fedb-4612-a4ae-261540d815ae"

def geocodificacion(location, key):
    while location == "":
        location = input("Ingresa la ubicación nuevamente: ")
    url_geocodificacion = "https://graphhopper.com/api/1/geocode?"
    url = url_geocodificacion + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

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

def CreateMap():
    
    m = folium.Map(location=[(origen[1] + destino[1]) / 2, (origen[2] + destino[2]) / 2], zoom_start=13)

    folium.Marker([origen[1], origen[2]], tooltip=origen[3], icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([destino[1], destino[2]], tooltip=destino[3], icon=folium.Icon(color='red')).add_to(m)

    print("\n Mapa Guardado Como 'Map.html'")
    m.save("Map.html")
    

while True:

    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("coche, bicicleta, a pie")
    print("+++++++++++++++++++++++++++++++++++++++++++++")

    perfiles = ["coche", "bicicleta", "a pie"]
    vehiculo = input("Ingresa un perfil de vehículo de la lista anterior: ")

    if vehiculo == "salir" or vehiculo == "s":
        break
    elif vehiculo in perfiles:
        vehiculo = vehiculo
    else:
        vehiculo = "coche"
        print("No se ingresó un perfil de vehículo válido. Se utilizará el perfil de coche.")

    loc1 = input("Ubicación de inicio: ")

    if loc1 == "salir" or loc1 == "s":
        break 
    
    origen = geocodificacion(loc1, key)
    print(origen)

    loc2 = input("Destino: ")
    
    if loc2 == "salir" or loc2 == "s":
        break
    
    destino = geocodificacion(loc2, key)
    print(destino)
    
    print("=================================================")

    if origen[0] == 200 and destino[0] == 200:
        op = "&point=" + str(origen[1]) + "%2C" + str(origen[2])
        dp = "&point=" + str(destino[1]) + "%2C" + str(destino[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehiculo": vehiculo}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print("Estado de la API de enrutamiento: " + str(paths_status) + "\nURL de la API de enrutamiento:\n" + paths_url)
        print("=================================================")
        print("Indicaciones desde " + origen[3] + " hasta " + destino[3] + " en " + vehiculo)
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

    CreateMap()