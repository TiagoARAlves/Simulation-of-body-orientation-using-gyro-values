import numpy as np
import draw

def rodriguesRotation(r, a, angle):
    scalar1 = (1 - np.cos(angle)) * (a[0] * r[0] + a[1] * r[1] + a[2] * r[2])
    scalar2 = np.cos(angle)
    scalar3 = np.sin(angle)
    b = [0, 0, 0]
    #       cos    *  v   +    sin  *   (k x v)                   +  (k * v)(1 - cos) * k
    b[0] = scalar2 * a[0] + scalar3 * (r[1] * a[2] - r[2] * a[1]) + scalar1 * r[0]
    b[1] = scalar2 * a[1] + scalar3 * (r[2] * a[0] - r[0] * a[2]) + scalar1 * r[1]
    b[2] = scalar2 * a[2] + scalar3 * (r[0] * a[1] - r[1] * a[0]) + scalar1 * r[2]
    return b

def frameMovimentation(base, angle):
    #X-axis rotation
    #Y
    aux = rodriguesRotation(base[0], base[1], angle[0])
    base[1][0] = aux[0]
    base[1][1] = aux[1]
    base[1][2] = aux[2]
    #Z
    aux = rodriguesRotation(base[0], base[2], angle[0])
    base[2][0] = aux[0]
    base[2][1] = aux[1]
    base[2][2] = aux[2]

    #Y-axis rotation
    #X
    aux = rodriguesRotation(base[1], base[0], angle[1])
    base[0][0] = aux[0]
    base[0][1] = aux[1]
    base[0][2] = aux[2]
    #Z
    aux = rodriguesRotation(base[1], base[2], angle[1])
    base[2][0] = aux[0]
    base[2][1] = aux[1]
    base[2][2] = aux[2]

    #Z-axis rotation
    #X
    aux = rodriguesRotation(base[2], base[0], angle[2])
    base[0][0] = aux[0]
    base[0][1] = aux[1]
    base[0][2] = aux[2]
    #Y
    aux = rodriguesRotation(base[2], base[1], angle[2])
    base[1][0] = aux[0]
    base[1][1] = aux[1]
    base[1][2] = aux[2]

    return base

def calculoFile(data, base, microSPerStep):
    f = open('output.txt', 'w')
    resto = 0
    f.write(f'{base[0][0]:0.2f};{base[0][1]:0.2f};{base[0][2]:0.2f};{base[1][0]:0.2f};{base[1][1]:0.2f};{base[1][2]:0.2f};{base[2][0]:0.2f};{base[2][1]:0.2f};{base[2][2]:0.2f}\n')
    for c in range(1, data[1:].size+1):
        deltaT = int(data[c][0]-data[c-1][0])    #Microssegundos 1s = 10^-6
        deltaT = deltaT + resto
        resto = deltaT%microSPerStep
        rotacoes = deltaT//microSPerStep
        xAnglePerStep = data[c][1]/1000000*microSPerStep
        yAnglePerStep = data[c][2]/1000000*microSPerStep
        zAnglePerStep = data[c][3]/1000000*microSPerStep
        for i in range(rotacoes):
            base = frameMovimentation(base, [xAnglePerStep, yAnglePerStep, zAnglePerStep])
        f.write(f'{base[0][0]:0.2f};{base[0][1]:0.2f};{base[0][2]:0.2f};{base[1][0]:0.2f};{base[1][1]:0.2f};{base[1][2]:0.2f};{base[2][0]:0.2f};{base[2][1]:0.2f};{base[2][2]:0.2f}\n')
    f.close()    
    return base

def calculoFileErrado(data, base):
    xAngle, yAngle, zAngle = 0, 0, 0
    for c in range(0, data[1:].size+1):
        xAngle = xAngle + data[c][1]
        yAngle = yAngle + data[c][2]
        zAngle = zAngle + data[c][3]
    base = frameMovimentation(base, [xAngle, yAngle, zAngle])
    
    return base

if __name__ == '__main__':
    #Prepara data
    try:
        with open('data.txt', 'r') as f:
            data = np.array(f.readlines())
            f.close()
    except IOError:
        print('Não existe o ficheiro \"data.txt\"! ')
        input('Pressione qualquer tecla para fechar o programa...')
        quit()
    data = np.char.strip(data, '\n')
    data = np.char.split(data, ';')
    for c in range(data.size):
        data[c] = np.array(data[c]).astype(np.single)

    microSPerStep = int(input('Numero de microsegundos para cada rotação sequencial: '))

    base = [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]

    #Correto
    base = calculoFile(data, base, microSPerStep)
    print('\n--------Calculo CORRETO--------')
    print('Valores finais')
    print('xb: ({}, {}, {}) \t\t ({:0.2f}, {:0.2f}, {:0.2f})'.format(base[0][0], base[0][1], base[0][2], base[0][0], base[0][1], base[0][2]))
    print('yb: ({}, {}, {}) \t\t ({:0.2f}, {:0.2f}, {:0.2f})'.format(base[1][0], base[1][1], base[1][2], base[1][0], base[1][1], base[1][2]))
    print('zb: ({}, {}, {}) \t\t ({:0.2f}, {:0.2f}, {:0.2f})'.format(base[2][0], base[2][1], base[2][2], base[2][0], base[2][1], base[2][2]))

    print('Norma dos vetores base: |xb|={:0.2f}, |yb|={:0.2f}, |zb|={:0.2f})\n'.format(np.sqrt(base[0][0]**2 + base[0][1]**2 + base[0][2]**2), np.sqrt(base[1][0]**2 + base[1][1]**2 + base[1][2]**2), np.sqrt(base[2][0]**2 + base[2][1]**2 + base[2][2]**2)))

    base = [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]
            
    #Errado
    base = calculoFileErrado(data, base)
    print('--------Calculo ERRADO--------')
    print('Valores finais')
    print('xb: ({}, {}, {}) \t\t ({:0.2f}, {:0.2f}, {:0.2f})'.format(base[0][0], base[0][1], base[0][2], base[0][0], base[0][1], base[0][2]))
    print('yb: ({}, {}, {}) \t\t ({:0.2f}, {:0.2f}, {:0.2f})'.format(base[1][0], base[1][1], base[1][2], base[1][0], base[1][1], base[1][2]))
    print('zb: ({}, {}, {}) \t\t ({:0.2f}, {:0.2f}, {:0.2f})'.format(base[2][0], base[2][1], base[2][2], base[2][0], base[2][1], base[2][2]))

    print('Norma dos vetores base: |xb|={:0.2f}, |yb|={:0.2f}, |zb|={:0.2f})\n\n'.format(np.sqrt(base[0][0]**2 + base[0][1]**2 + base[0][2]**2), np.sqrt(base[1][0]**2 + base[1][1]**2 + base[1][2]**2), np.sqrt(base[2][0]**2 + base[2][1]**2 + base[2][2]**2)))

    simular = input("Deseja simular o movimento do corpo? [s/n]: ")
    if(simular=="s" or simular=="S"):
        draw.simula()

    input('\n\nPressione qualquer tecla para fechar o programa...')