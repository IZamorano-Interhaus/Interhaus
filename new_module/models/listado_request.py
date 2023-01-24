class importData():
    def __init__(self, rutTrib,folio,tipoDoc,doc):
           self.__rutTributario = rutTrib
           self.__folioDocumento = folio
           self.__documento= doc
           self.__tipoDocumento=tipoDoc
        #getters

    def get_rut(self):
         return self.__rutTributario

    def get_folio(self):
         return self.__folioDocumento
      
    def get_tipoDocumento(self):
        
            
        return self.__tipoDocumento

    def get_documento(self):
        if self.get_tipoDocumento()==30:
            self.__documento="factura"
        elif self.get_tipoDocumento()==32:
            self.doc="factura de ventas y servicios no afectos o exentos de IVA"
        else:
            print("error")        
        return self.__documento
    #setters

    def set_rut(self,rutTributario):
        self.__rutTributario=rutTributario
    
    #metodos
    
      

      
auxList=[]
mensaje = importData(19669468-4,123541,30,"factura")

print(mensaje.get_documento()," | ",mensaje.get_tipoDocumento())
auxList.append(mensaje.get_rut())
auxList.append(mensaje.get_folio())
auxList.append(mensaje.get_documento())
auxList.append(mensaje.get_tipoDocumento())
print(auxList)

""" 

    30 Factura
    32 Factura de ventas y servicios no afectos o exentos de IVA
    33 Factura electrónica
    34 Factura no afecta o exenta electrónica
    35 Boleta
    38 Boleta exenta
    39 Boleta electrónica
    40 Liquidación factura
    41 Boleta exenta electrónica
    43 Liquidación factura electrónica
    45 Factura de compra
    46 Factura de compra electrónica
    48 Pago electrónico
    50 Guía de despacho
    52 Guía de despacho electrónica
    55 Nota de débito
    56 Nota de débito electrónica
    60 Nota de crédito
    61 Nota de crédito electrónica
    103 Liquidación
    110 Factura de exportación electrónica
    111 Nota de débito de exportación electrónica
    112 Nota de crédito de exportación electrónica
 """