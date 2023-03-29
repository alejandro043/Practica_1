from email.policy import default
from reportlab.pdfgen import canvas
from pysnmp.hlapi import *
from reportlab.platypus import *


def agregarAgente():  
    print("Agregar Agente")
    comunidad = input("Comunidad: ")
    version = input("Version SNMP: ")
    puerto = '161'
    ip = input("IP: ")
    agentes = comunidad + " " + version + " " + puerto + " " + ip 
    print(agentes)
    file = open("Agentes.txt",'a')
    file.write(agentes)
    file.write("\n")
    file.close()
    print("Agente agregado..\n")
  
  
def eliminarAgente():
    print("Eliminar agente")
    elimi = open("Agentes.txt",'r')
    agentes = elimi.readlines()
    elimi.close()
    print("Se han capturado ", len(agentes) ,"agentes...")
    selec = input("Seleccione un agente para eliminar: ")
    op = int(selec)-1
    if op > len(agentes):
        print("Fuera del limite de agentes, selecciona una respuesta correcta")
        eliminarAgente()
    else:
        elimi = open("Agentes.txt", 'w')
        index=0
        while index < len(agentes) :
            if index != op:
                elimi.write(agentes[index])
                if index != len(agentes) - 1:
                    elimi.write("\n")
            index+=1
        elimi.close()
    print("Agente eliminado...\n")


def generarReporte():
    print("Reporte en pdf")
    pdf = open("Agentes.txt",'r')
    agentes = pdf.readlines()
    pdf.close()
    age = input("Seleccione el index de un agente para generar su reporte: ")
    op= int(age)
    datos = agentes[op].split()
    print(datos)
    
    consulta = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.1.0")
    ewe=consulta.split()
    so=consulta[1] + consulta[2] + consulta[3] + consulta[4] + consulta[5]
    nombre = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.5.0")
    contacto = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.4.0")
    ubicacion = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.1.6.0")
    numInterfaces = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.1.0")
   
    cont = 1
    interfaces = []
    while cont<=int(numInterfaces) and cont < 6:
        cuentaIn = consultaSNMP(datos[0],datos[3],'1.3.6.1.2.1.2.2.1.7.' + str(cont))
        interfaces.append(cuentaIn)
        cont+=1
   
    a = 1
    arregloInterfaz = [["Descripcion","Estado"]]
    while a<=len(interfaces):
        if so.find("Linux") != -1:
            descripcion = consultaSNMP(datos[0], datos[3], "1.3.6.1.2.1.2.2.1.2."+str(a))
        else:
            otros = consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.2.1.2."+str(a))[3:]
            descripcion = bytes.fromhex(otros).decode('UTF-8')
        statusInterface=consultaSNMP(datos[0],datos[3],"1.3.6.1.2.1.2.2.1.7."+str(a))
        if statusInterface=="1":
            arregloInterfaz.append([descripcion,'Up'])
        elif statusInterface=="2":
            arregloInterfaz.append([descripcion,'Down'])
        else:
            arregloInterfaz.append([descripcion,'Testing'])
        # print(descripcion, statusInterface)
        a += 1
    
    
   
    report = canvas.Canvas("reporteAgente.pdf")
    report.setTitle("Reporte SNMP")
    report.drawString(50, 750, "U.A: Administración de Servicios en Red")
    report.drawString(50, 725, "Práctica 1 -> Adquisicion de información")
    report.drawString(50, 700, "ALEJANDRO ROSAS ARRIETA      4CM14        2020630413")
    report.drawString(230,635,"REPORTE AGENTE")
    report.drawString(50,600, "Sistema operativo: " + so)
    report.drawString(50,575, "Nombre del dispositivo: " + nombre)
    report.drawString(50,550, "Contacto: " + contacto)
    report.drawString(50,525, "Ubicación: " + ubicacion)
    report.drawString(50,500, "Número de interfaces: " + numInterfaces)
    if so == 'Linux':
    	report.drawString(50,250,"Logo S.O")
    	report.drawImage('linux.png',50,30,width=200,height=200)
    else:
    	report.drawImage('windows.png',50,30,width=200,height=200)
    
    tabla = Table(arregloInterfaz)
    tabla.wrapOn(report,200,400)
    tabla.drawOn(report,50,350)
    
    report.save()
    print("Reporte generado...\n")
    




def consultaSNMP(comunidad,ip,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad,mpModel=0),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado = varB.split("=")[1]
            return resultado



    
def salir():
    print("Fin del programa...")





def menu():
    op = 0
    while op != 4:
    	
        print("|--------Elige una opcion--------|")
        print("|--------------------------------|")
        print("|        1-> Agregar             |")

        print("|        2-> Eliminar            |")

        print("|        3-> Generar reporte     |")

        print("|        4-> Salir               |")

        op = int(input("Que desea hacer?:"))
        
        if op==1:
            agregarAgente()
        elif op==2:
            eliminarAgente()
        elif op==3:
            generarReporte()
        elif op==4:
            salir()

print("\t  Sistema de Administración de red")
print("\tPractica 1 -> Adquisición de información")
print("\tRosas Arrieta Alejandro \t \t 2020630413")
menu()
