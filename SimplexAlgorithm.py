#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 3 13:53:38 2021

@author: darios
"""

import numpy as np

#Inicializamos una matriz vacía para poder empezar el código
renglones=int(input("Número de restricciones "))
columnas=int(input("Número de variables "))
mat = np.zeros((renglones, columnas+renglones))

#Llenar la matriz
for r in range(0,renglones):
    for c in range(0,columnas):
        #En esta línea r y c sirven para guiarte en el renglón y columna en el que se encuentra el ciclo
        mat[(r),(c)]=(input("Elemento a["+str(r)+","+str(c)+"] "))

vectorb=np.zeros(renglones)
for i in range(0, renglones):
    vectorb[i]=float(input("Pon el valor de la capacidad de la restricción "+str(i+1)+": "))
    
#Ponemos las variables de holgura o de exceso y armamos el vector b
for r in range(0, renglones):
    hol=int(input("Pon '1' si tu restricción "+str(r+1)+" va a necesitar variable de holgura o '0' si necesita variable de exceso "))
    if (hol==0):
        for c in range(0, columnas):
            mat[(r), (c)]=(-1)*mat[(r), (c)]
            vectorb[r]=vectorb[r]*(-1)
    #Estas líneas son las que arman la parte de la matriz con las variables de holgura o de exceso
    for c in range(columnas, columnas+renglones):
        if (r+columnas==c):
            mat[(r), (c)]=1
        else:
            mat[(r), (c)]=0

#Vamos a armar el vector c
vectorc=np.zeros(columnas+renglones)

for i in range(0, columnas+renglones):
    if (i<columnas):
        vectorc[i]=float(input("Pon el valor de los coeficientes de la función de maximización o minimización: "))

#Preguntamos si se quiere maximizar o minimizar el problema
tipo=int(input("Pon '1' si quieres maximizar o '0' si quieres minimizar."))


print(vectorb)
print(vectorc)
print(mat)
print(tipo)


#Tomamos como primera base a las variables de holgura o de exceso. Inicializamos la matriz B.
matB=np.zeros((renglones, renglones))

#Armamos la matriz B con los números de la matriz con las variables de holgura.
for r in range(0, renglones):
    for c in range(0, renglones):
        if (r==c):
            matB[(r), (c)]=mat[(r), (columnas+c)]

#Estas líneas solo están aquí para inicializar las variables de los índices, aquí son irrelevantes, pero se usan después.
indiceentrada=renglones+columnas-1
indicesalida=0

#Inicializamos el vector CB.
vectorcb=np.zeros(renglones)

#hacemos la operación del primer cuadrado
#aux1=np.matmul(np.matmul(vectorcb, matBinv), mat)-vectorc

#Inicializamos una matriz que pueda contener los cuatro cuadros
matsimp=np.zeros((renglones+1, renglones+columnas+1))

#Empezamos el algoritmo Simplex, tenemos que ver si hay números negativos en el primer cuadrado.
var1=False

#Mientras haya números negativos en el primer cuadrado del algoritmo, este while se va a repetir.
if (tipo==1):
    print("Maximización")
    while (var1==False):
        #Sacamos la matriz inversa de B
        matBinv=np.linalg.inv(matB)
        #Armamos o cambiamos el vector cb
        vectorcb[indicesalida]=vectorc[indiceentrada]
        #Armamos el cuadrado de la esquina superior izquierda
        aux1=np.matmul(np.matmul(vectorcb, matBinv), mat)-vectorc
        #Ponemos el vector aux1 en la matriz matsimp
        for i in range(0, renglones+columnas):
            matsimp[(0), (i)]=aux1[i]
            print(aux1[i])
        #Vamos a ver si se tiene que seguir en el ciclo.
        for i in range(0, len(aux1)):
            if (np.min(aux1)<0):
                var1=False
            else:
                var1=True
                break
        for i in range(0, renglones+columnas):
            matsimp[(0), (i)]=aux1[i]
            #Armamos el cuadrado de la esquina inferior izquierda y lo metemos a la matriz del método Simplex.
            aux2=np.matmul(matBinv, mat)
        for i in range(1, renglones+1):
            for j in range(0, renglones+columnas):
                matsimp[(i), (j)]=aux2[(i-1), (j)]
        #Armamos el cuadrado de la esquina superior derecha y lo metemos a la matriz del método Simplex.
        aux3=np.matmul(np.matmul(vectorcb, matBinv), vectorb)
        matsimp[(0), renglones+columnas]=aux3
        #Armamos el cuadrado de la esquina inferior derecha y lo metemos a la matriz del método Simplex.
        aux4=np.matmul(matBinv, vectorb)
        for j in range(1, renglones+1):
            matsimp[(j), (renglones+columnas)]=aux4[j-1]
        #Sacamos el valor mínimo de la fila de las variables básicas
        varmin=10
        for i in range(0, len(aux1)):
            if (matsimp[(0), (i)]<varmin):
                print(i)
                varmin=matsimp[(0),(i)]
                indiceentrada=i
        #Declaramos un vector auxiliar para hacer la división entre coeficientes de las variables que van a entrar y salir
        vecauxentsal=np.zeros(renglones)
        for i in range(1, renglones+1):
            vecauxentsal[i-1]=matsimp[(i),(renglones+columnas)]/matsimp[(i), (indiceentrada)]
        #Tomamos el valor mínimo del vector resultante.
        valormin=np.min(vecauxentsal) 
        indicesalida=20
        #Tomamos el índice del valor mínimo para ver cuál variable va a ser la que va a salir.
        for i in range(1, renglones+1):
            if (vecauxentsal[i-1]==valormin):
                indicesalida=i-1
        #modificamos la matriz B
        for i in range(0, renglones):
            matB[(i), (indicesalida)]=mat[(i), (indiceentrada)]
        print(matsimp)
elif(tipo==0):
    print("Minimización")
    while (var1==False):
        #Sacamos la matriz inversa de B
        matBinv=np.linalg.inv(matB)
        #Armamos o cambiamos el vector cb
        vectorcb[indicesalida]=vectorc[indiceentrada]
        #Armamos el cuadrado de la esquina superior izquierda
        aux1=np.matmul(np.matmul(vectorcb, matBinv), mat)-vectorc
        #Ponemos el vector aux1 en la matriz matsimp
        for i in range(0, renglones+columnas):
            matsimp[(0), (i)]=aux1[i]
        #Vamos a ver si se tiene que seguir en el ciclo.
        for i in range(0, len(aux1)):
            if (np.min(aux1)<0):
                var1=False
            else:
                var1=True
                break
        for i in range(0, renglones+columnas):
            matsimp[(0), (i)]=aux1[i]
            #Armamos el cuadrado de la esquina inferior izquierda y lo metemos a la matriz del método Simplex.
            aux2=np.matmul(matBinv, mat)
        for i in range(1, renglones+1):
            for j in range(0, renglones+columnas):
                matsimp[(i), (j)]=aux2[(i-1), (j)]
        #Armamos el cuadrado de la esquina superior derecha y lo metemos a la matriz del método Simplex.
        aux3=np.matmul(np.matmul(vectorcb, matBinv), vectorb)
        matsimp[(0), renglones+columnas]=aux3
        #Armamos el cuadrado de la esquina inferior derecha y lo metemos a la matriz del método Simplex.
        aux4=np.matmul(matBinv, vectorb)
        for j in range(1, renglones+1):
            matsimp[(j), (renglones+columnas)]=aux4[j-1]
        #Sacamos el valor mínimo de la columna de las variables de solución.
        varmin=10
        for i in range(1, renglones+1):
            if (matsimp[(i), (columnas+renglones)]<varmin):
                varmin=matsimp[(i),(columnas+renglones)]
                indiceentrada=i-1
        #Declaramos un vector lleno de números grandes para poder sacar las divisiones.
        vecauxentsal=np.zeros(renglones+columnas)
        """
        for i in range(0, len(vecauxentsal)):
            vecauxentsal[i]=vecauxentsal[i]*400
        """
        for i in range(0, renglones):
            if (matsimp[(indiceentrada+1),(i)]<0):
                vecauxentsal[i]=np.abs(vectorc[i]/matsimp[(indiceentrada+1),(i)])
        #Checamos cuál es el valor mínimo.
        valormin=10000
        for i in range(0, renglones+columnas):
            if (vecauxentsal[i]!=0):
                if (vecauxentsal[i]<valormin):
                    valormin=vecauxentsal[i]
                    indicesalida=i
                    print("Linea198")
        #valormin=np.min(vecauxentsal)
        #indicesalida=40000
        #Vemos cuál variable va a ser la que va a salir.
        for i in range(0, renglones+columnas):
            if (vecauxentsal[i]==valormin):
                indicesalida=i
        print("Indice salida", indicesalida)
        print("Indice entrada", indiceentrada)
        #modificamos la matriz B
        for i in range(0, renglones):
            matB[(i), (indicesalida)]=mat[(i), (indiceentrada)]
        print(matsimp)
        #Vamos a checar si tenemos que volver a entrar al while o ya nos salimos
        boolaux=False
        for i in range(0, renglones+columnas):
            if (matsimp[(indicesalida),(i)]<0):
                boolaux=True
        if (boolaux==False):
            var1=True
else:
    print("Esa opción no existe")
  
print("La solución del problema es: "+str(matsimp[(0), (renglones+columnas)]))
print("La matriz de la solución del problema está dada por: ")
print(matsimp)
