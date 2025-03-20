class subneting:
    """
    Clase para realizar cálculos de subnetting de redes IPv4.
    Permite calcular direcciones de red, broadcast, hosts utilizables
    y otras propiedades a partir de una dirección IP y su máscara.
    """
    def __init__(self, ip, mascara):
        """
        Inicializa una instancia de la clase con una dirección IP y una máscara de subred.
        
        Args:
            ip (str): Dirección IP en formato decimal puntuado (ej. "192.168.1.100")
            mascara (int): Longitud del prefijo de red en bits (ej. 24 para /24)
        """
        self.ip = ip
        self.mascara = mascara

    def binario(self, num):
        """
        Convierte un número decimal a su representación binaria de 8 bits.
        
        Args:
            num (int): Número decimal a convertir (0-255)
            
        Returns:
            list: Lista de 8 dígitos binarios (0 o 1)
        """
        # Calcula el binario por metodo de sacar modulos de 2
        num = int(num)
        binario = []

        while (num > 0):
            resto = num % 2
            binario.insert(0, resto)
            num = num // 2

        # Corrige la longitud del binario y que debe de tener 8 caracteres estrictos añadiendo 0s al principio
        lon = 8 - int(len(binario))

        for i in range(lon):
            binario.insert(0, 0)

        return binario

    def decimal(self, bin):
        """
        Convierte una representación binaria a formato decimal puntuado.
        
        Args:
            bin (list): Lista de dígitos binarios (0 o 1)
            
        Returns:
            str: Representación decimal puntuada (ej. "192.168.1.0")
        """
        l = 8
        mi_ip = ""
        cont = 0

        # Divide la ip en octetos
        for i in range(0, len(bin), l):
            output = bin[i:i + l] 

            # Calcula el numero decimal sumando las potencias de 2 correspondientes
            a = 128
            for i in output:
                if i == 0:
                    pass
                else:
                    cont = cont + a
                a = a / 2

            cont = int(cont)
            mi_ip = mi_ip + str(cont) + "."
            cont = 0
        
        return mi_ip[:-1]  # Elimina el último punto

    def ip_bin(self):
        """
        Convierte la dirección IP de la instancia a su representación binaria.
        
        Returns:
            list: Lista de 32 dígitos binarios representando la dirección IP
        """
        ip = self.ip
        nume = ""
        ipenbin = []

        # Saca los números de la IP separada por "."
        for i in ip:
            if i != ".":
                nume = nume + i 
            else:
                ipenbin += self.binario(nume)
                nume = ""
        
        # Utiliza la función binario para convertir el último octeto
        ipenbin += self.binario(nume)

        return ipenbin

    def masc(self):
        """
        Calcula la representación binaria de la máscara de subred.
        
        Returns:
            list: Lista de 32 dígitos binarios representando la máscara
        """
        masc = self.mascara
        masc = masc - 1
        l_masc = []

        # Crea la máscara en binario (1s para bits de red, 0s para bits de host)
        for i in range(32):
            if i <= masc:
                l_masc.append(1)
            else:
                l_masc.append(0)
            
        return l_masc

    def ip_red(self):
        """
        Calcula la dirección de red aplicando la operación AND entre
        la dirección IP y la máscara de subred.
        
        Returns:
            str: Dirección de red en formato decimal puntuado
        """
        # Aplica la máscara a la IP para obtener la dirección de red
        y = self.ip_bin()
        x = self.masc()

        for i in range(32):
            if x[i] == 0:
                y[i] = 0

        return self.decimal(y)
        
    def primer_host(self):
        """
        Calcula la dirección del primer host utilizable en la subred.
        Es la dirección de red más 1.
        
        Returns:
            str: Dirección del primer host en formato decimal puntuado
        """
        y = self.ip_bin()
        x = self.masc()

        for i in range(32):
            if x[i] == 0:
                y[i] = 0
        
        y[31] = 1  # Último bit a 1 para obtener primer host

        return self.decimal(y)

    def ip_broadcast(self):
        """
        Calcula la dirección de broadcast de la subred.
        Todos los bits de host se establecen a 1.
        
        Returns:
            str: Dirección de broadcast en formato decimal puntuado
        """
        # Aplica la máscara inversa a la IP para obtener la dirección de broadcast
        y = self.ip_bin()
        x = self.masc()
        
        for i in range(32):
            if x[i] == 0:
                y[i] = 1

        return self.decimal(y)

    def ultimo_host(self):
        """
        Calcula la dirección del último host utilizable en la subred.
        Es la dirección de broadcast menos 1.
        
        Returns:
            str: Dirección del último host en formato decimal puntuado
        """
        y = self.ip_bin()
        x = self.masc()
        
        for i in range(32):
            if x[i] == 0:
                y[i] = 1
        y[31] = 0  # Penúltimo bit a 0 para obtener último host

        return self.decimal(y)

    def num_hosts(self):
        """
        Calcula el número de hosts utilizables en la subred.
        Fórmula: 2^(bits de host) - 2
        Se restan 2 para excluir la dirección de red y broadcast.
        
        Returns:
            int: Número de hosts utilizables
        """
        bits_host = 32 - self.mascara
        # Restamos 2 para excluir la dirección de red y broadcast
        hosts = (2 ** bits_host) - 2
        
        return hosts
    
    def mostrar_info_subred(self):
        """
        Recopila toda la información calculada de la subred en un diccionario.
        
        Returns:
            dict: Diccionario con información completa de la subred
        """
        info = {
            "Dirección IP": self.ip,
            "Máscara (prefijo)": f"/{self.mascara}",
            "Máscara (decimal)": self.decimal(self.masc()),
            "Dirección de red": self.ip_red(),
            "Primer host utilizable": self.primer_host(),
            "Último host utilizable": self.ultimo_host(),
            "Dirección de broadcast": self.ip_broadcast(),
            "Número de hosts utilizables": self.num_hosts()
        }
        
        return info
    