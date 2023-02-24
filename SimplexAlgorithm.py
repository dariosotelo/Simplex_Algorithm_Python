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

#These lines initialize the index variables, they are not used here, but they become relevant afterwards
entryIndex=row+columns-1
exitIndex=0

#This is to initialize the Cb vector
vectorcb=np.zeros(row)

#A matrix that can hold four squares is initialized
matsimp=np.zeros((row+1, row+columns+1))

#The Simplex Algorithm is started, it has to look out for negative numbers in the first square.
var1=False

#As long as there are negative numbers in the first square of the algorithm, this code is going to loop.
if (typ==1):
    print("Maximization")
    while (var1==False):
        #The inverse matrix of B
        matBinv=np.linalg.inv(matB)
        #The cb vector is created or modified.
        vectorcb[exitIndex]=vectorc[entryIndex]
        #This operation is to get the first square of the top left corner
        aux1=np.matmul(np.matmul(vectorcb, matBinv), mat)-vectorc
        #The aux1 vector is inserted to the matsimp matrix
        for i in range(0, row+columns):
            matsimp[(0), (i)]=aux1[i]
            print(aux1[i])
        #These lines of code check if the loop is continued.
        for i in range(0, len(aux1)):
            if (np.min(aux1)<0):
                var1=False
            else:
                var1=True
                break
        for i in range(0, row+columns):
            matsimp[(0), (i)]=aux1[i]
            #The bottom lef square is created and inserted into the simplex method matrix.
            aux2=np.matmul(matBinv, mat)
        for i in range(1, row+1):
            for j in range(0, row+columns):
                matsimp[(i), (j)]=aux2[(i-1), (j)]
        #The top right square is created and inserted into the simplex method matrix.
        aux3=np.matmul(np.matmul(vectorcb, matBinv), vectorb)
        matsimp[(0), row+columns]=aux3
        #The bottom right square is created and inserted into the simplex method matrix.
        aux4=np.matmul(matBinv, vectorb)
        for j in range(1, row+1):
            matsimp[(j), (row+columns)]=aux4[j-1]
        #The minimum value of the row of basic variables is selected.
        varmin=10
        for i in range(0, len(aux1)):
            if (matsimp[(0), (i)]<varmin):
                print(i)
                varmin=matsimp[(0),(i)]
                entryIndex=i
        #There is an auxiliar vector created to make the division between coefficients of the variables who are going to enter and exit.
        auxVecEntEx=np.zeros(row)
        for i in range(1, row+1):
            auxVecEntEx[i-1]=matsimp[(i),(row+columns)]/matsimp[(i), (entryIndex)]
        #The minimum value of the resultant vector is chosen.
        minVal=np.min(auxVecEntEx) 
        exitIndex=20
        #The index of the minimum value is chosen to exit.
        for i in range(1, row+1):
            if (auxVecEntEx[i-1]==minVal):
                exitIndex=i-1
        #the B matrix is modified
        for i in range(0, row):
            matB[(i), (exitIndex)]=mat[(i), (entryIndex)]
        print(matsimp)
elif(typ==0):
    print("Minimization")
    while (var1==False):
        #The inverse of the B matrix
        matBinv=np.linalg.inv(matB)
        #The cb vector is created of modified.
        vectorcb[exitIndex]=vectorc[entryIndex]
        #The top left corner square is created.
        aux1=np.matmul(np.matmul(vectorcb, matBinv), mat)-vectorc
        #The aux1 vector is inserted into the matsimp matrix.
        for i in range(0, row+columns):
            matsimp[(0), (i)]=aux1[i]
        #These lines check if the loop is necessary to continue.
        for i in range(0, len(aux1)):
            if (np.min(aux1)<0):
                var1=False
            else:
                var1=True
                break
        for i in range(0, row+columns):
            matsimp[(0), (i)]=aux1[i]
            #the bottom left corner square is created and inserted into the simplex matrix.
            aux2=np.matmul(matBinv, mat)
        for i in range(1, row+1):
            for j in range(0, row+columns):
                matsimp[(i), (j)]=aux2[(i-1), (j)]
        #the top right corner square is created and inserted into the simplex matrix.
        aux3=np.matmul(np.matmul(vectorcb, matBinv), vectorb)
        matsimp[(0), row+columns]=aux3
        #the bottom right square is created and inserted into the simplex matrix.
        aux4=np.matmul(matBinv, vectorb)
        for j in range(1, row+1):
            matsimp[(j), (row+columns)]=aux4[j-1]
        #the minimum value of the columns.
        varmin=10
        for i in range(1, row+1):
            if (matsimp[(i), (columns+row)]<varmin):
                varmin=matsimp[(i),(columns+row)]
                entryIndex=i-1
        #this is a vector filled with big numbers so we can get the divisions
        auxVecEntEx=np.zeros(row+columns)
        for i in range(0, row):
            if (matsimp[(entryIndex+1),(i)]<0):
                auxVecEntEx[i]=np.abs(vectorc[i]/matsimp[(entryIndex+1),(i)])
        #the minimum value is selected.
        minVal=10000
        for i in range(0, row+columns):
            if (auxVecEntEx[i]!=0):
                if (auxVecEntEx[i]<minVal):
                    minVal=auxVecEntEx[i]
                    exitIndex=i
                    print("Linea198")
        #this code is to check which variable will exit.
        for i in range(0, row+columns):
            if (auxVecEntEx[i]==minVal):
                exitIndex=i
        print("Exit index ", exitIndex)
        print("Entry index ", entryIndex)
        #the B matrix is modified.
        for i in range(0, row):
            matB[(i), (exitIndex)]=mat[(i), (entryIndex)]
        print(matsimp)
        #This code checks if it is necessary to repeat the loop.
        boolaux=False
        for i in range(0, row+columns):
            if (matsimp[(exitIndex),(i)]<0):
                boolaux=True
        if (boolaux==False):
            var1=True
else:
    print("That option does not exist. ")
  
print("The solution of the problem is: "+str(matsimp[(0), (row+columns)]))
print("The matrix of the solution of the problem is: ")
print(matsimp)
