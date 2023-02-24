#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 3 13:53:38 2021

@author: darios
"""

import numpy as np

#We initialize an empty matrix to start the code.
row=int(input("Número de restricciones "))
columns=int(input("Número de variables "))
mat = np.zeros((row, columns+row))

#Fill up the matrix.
for r in range(0,row):
    for c in range(0,columns):
        #In this line r and c are used to guide the user in which value to insert.
        mat[(r),(c)]=(input("Element a["+str(r)+","+str(c)+"] "))

vectorb=np.zeros(row)
for i in range(0, row):
    vectorb[i]=float(input("Insert the value of the capacity of the restriction "+str(i+1)+": "))

#We insert the slack or excess variables and build up the b vector.
for r in range(0, row):
    hol=int(input("Press '1' if your "+str(r+1)+"° restriction will need a slack variable or '0' if it needs an excess variable "))
    if (hol==0):
        for c in range(0, columns):
            mat[(r), (c)]=(-1)*mat[(r), (c)]
            vectorb[r]=vectorb[r]*(-1)
    #These lines of code build up the matrix including the excess and/or slack variables.
    for c in range(columns, columns+row):
        if (r+columns==c):
            mat[(r), (c)]=1
        else:
            mat[(r), (c)]=0

#These lines build up the c vector.
vectorc=np.zeros(columns+row)

for i in range(0, columns+row):
    if (i<columns):
        vectorc[i]=float(input("Insert the value of the coefficients of the optimization function: "))

#The user is asked whether it wants to minimize or maximize the problem.
typ=int(input("Press '1' if you want to maximize or press '0' if you want to minimize. "))


print(vectorb)
print(vectorc)
print(mat)
print(typ)


#We use the variables of slack or excess as the first base, we initialize the B matrix.
matB=np.zeros((row, row))

for r in range(0, row):
    for c in range(0, row):
        if (r==c):
            matB[(r), (c)]=mat[(r), (columns+c)]

#Estas líneas solo están aquí para inicializar las variables de los índices, aquí son irrelevantes, pero se usan después.
entryIndex=row+columns-1
exitIndex=0

#Inicializamos el vector CB.
vectorcb=np.zeros(row)

#hacemos la operación del primer cuadrado
#aux1=np.matmul(np.matmul(vectorcb, matBinv), mat)-vectorc

#Inicializamos una matrix que pueda contener los cuatro cuadros
matsimp=np.zeros((row+1, row+columns+1))

#Empezamos el algoritmo Simplex, tenemos que ver si hay números negativos en el primer cuadrado.
var1=False

#Mientras haya números negativos en el primer cuadrado del algoritmo, este while se va a repetir.
if (typ==1):
    print("Maximización")
    while (var1==False):
        #Sacamos la matrix inversa de B
        matBinv=np.linalg.inv(matB)
        #Armamos o cambiamos el vector cb
        vectorcb[exitIndex]=vectorc[entryIndex]
        #Armamos el cuadrado de la esquina superior izquierda
        aux1=np.matmul(np.matmul(vectorcb, matBinv), mat)-vectorc
        #Ponemos el vector aux1 en la matrix matsimp
        for i in range(0, row+columns):
            matsimp[(0), (i)]=aux1[i]
            print(aux1[i])
        #Vamos a ver si se tiene que seguir en el ciclo.
        for i in range(0, len(aux1)):
            if (np.min(aux1)<0):
                var1=False
            else:
                var1=True
                break
        for i in range(0, row+columns):
            matsimp[(0), (i)]=aux1[i]
            #Armamos el cuadrado de la esquina inferior izquierda y lo metemos a la matrix del método Simplex.
            aux2=np.matmul(matBinv, mat)
        for i in range(1, row+1):
            for j in range(0, row+columns):
                matsimp[(i), (j)]=aux2[(i-1), (j)]
        #Armamos el cuadrado de la esquina superior derecha y lo metemos a la matrix del método Simplex.
        aux3=np.matmul(np.matmul(vectorcb, matBinv), vectorb)
        matsimp[(0), row+columns]=aux3
        #Armamos el cuadrado de la esquina inferior derecha y lo metemos a la matrix del método Simplex.
        aux4=np.matmul(matBinv, vectorb)
        for j in range(1, row+1):
            matsimp[(j), (row+columns)]=aux4[j-1]
        #Sacamos el valor mínimo de la fila de las variables básicas
        varmin=10
        for i in range(0, len(aux1)):
            if (matsimp[(0), (i)]<varmin):
                print(i)
                varmin=matsimp[(0),(i)]
                entryIndex=i
        #Declaramos un vector auxiliar para hacer la división entre coeficientes de las variables que van a entrar y salir
        auxVecEntEx=np.zeros(row)
        for i in range(1, row+1):
            auxVecEntEx[i-1]=matsimp[(i),(row+columns)]/matsimp[(i), (entryIndex)]
        #Tomamos el valor mínimo del vector resultante.
        minVal=np.min(auxVecEntEx) 
        exitIndex=20
        #Tomamos el índice del valor mínimo para ver cuál variable va a ser la que va a salir.
        for i in range(1, row+1):
            if (auxVecEntEx[i-1]==minVal):
                exitIndex=i-1
        #modificamos la matrix B
        for i in range(0, row):
            matB[(i), (exitIndex)]=mat[(i), (entryIndex)]
        print(matsimp)
elif(typ==0):
    print("Minimización")
    while (var1==False):
        #Sacamos la matrix inversa de B
        matBinv=np.linalg.inv(matB)
        #Armamos o cambiamos el vector cb
        vectorcb[exitIndex]=vectorc[entryIndex]
        #Armamos el cuadrado de la esquina superior izquierda
        aux1=np.matmul(np.matmul(vectorcb, matBinv), mat)-vectorc
        #Ponemos el vector aux1 en la matrix matsimp
        for i in range(0, row+columns):
            matsimp[(0), (i)]=aux1[i]
        #Vamos a ver si se tiene que seguir en el ciclo.
        for i in range(0, len(aux1)):
            if (np.min(aux1)<0):
                var1=False
            else:
                var1=True
                break
        for i in range(0, row+columns):
            matsimp[(0), (i)]=aux1[i]
            #Armamos el cuadrado de la esquina inferior izquierda y lo metemos a la matrix del método Simplex.
            aux2=np.matmul(matBinv, mat)
        for i in range(1, row+1):
            for j in range(0, row+columns):
                matsimp[(i), (j)]=aux2[(i-1), (j)]
        #Armamos el cuadrado de la esquina superior derecha y lo metemos a la matrix del método Simplex.
        aux3=np.matmul(np.matmul(vectorcb, matBinv), vectorb)
        matsimp[(0), row+columns]=aux3
        #Armamos el cuadrado de la esquina inferior derecha y lo metemos a la matrix del método Simplex.
        aux4=np.matmul(matBinv, vectorb)
        for j in range(1, row+1):
            matsimp[(j), (row+columns)]=aux4[j-1]
        #Sacamos el valor mínimo de la columna de las variables de solución.
        varmin=10
        for i in range(1, row+1):
            if (matsimp[(i), (columns+row)]<varmin):
                varmin=matsimp[(i),(columns+row)]
                entryIndex=i-1
        #Declaramos un vector lleno de números grandes para poder sacar las divisiones.
        auxVecEntEx=np.zeros(row+columns)
        """
        for i in range(0, len(auxVecEntEx)):
            auxVecEntEx[i]=auxVecEntEx[i]*400
        """
        for i in range(0, row):
            if (matsimp[(entryIndex+1),(i)]<0):
                auxVecEntEx[i]=np.abs(vectorc[i]/matsimp[(entryIndex+1),(i)])
        #Checamos cuál es el valor mínimo.
        minVal=10000
        for i in range(0, row+columns):
            if (auxVecEntEx[i]!=0):
                if (auxVecEntEx[i]<minVal):
                    minVal=auxVecEntEx[i]
                    exitIndex=i
                    print("Linea198")
        #minVal=np.min(auxVecEntEx)
        #exitIndex=40000
        #Vemos cuál variable va a ser la que va a salir.
        for i in range(0, row+columns):
            if (auxVecEntEx[i]==minVal):
                exitIndex=i
        print("Indice salida", exitIndex)
        print("Indice entrada", entryIndex)
        #modificamos la matrix B
        for i in range(0, row):
            matB[(i), (exitIndex)]=mat[(i), (entryIndex)]
        print(matsimp)
        #Vamos a checar si tenemos que volver a entrar al while o ya nos salimos
        boolaux=False
        for i in range(0, row+columns):
            if (matsimp[(exitIndex),(i)]<0):
                boolaux=True
        if (boolaux==False):
            var1=True
else:
    print("Esa opción no existe")
  
print("La solución del problema es: "+str(matsimp[(0), (row+columns)]))
print("La matrix de la solución del problema está dada por: ")
print(matsimp)
