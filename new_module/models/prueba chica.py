import json, os ,psycopg2
os.system('cls')
auxlista2=[]
auxlista1=[]
listaFinal=[]
listaRut=[]
l=[]
conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
cur = conn.cursor()
f = open("C:/tools/respaldoBaseDatos/SIIpruebas.json", "r")
archivoJSON = f.read()
datosJSON = json.loads(archivoJSON)
for ingreso in (datosJSON["ventas"]["detalleVentas"]):
    lax=[]
    lax=ingreso["tipoDTEString"	  ],
    str(ingreso["tipoDTE"      	  ]),
    ingreso["tipoCompra"   	  ],
    ingreso["rutCliente"   	  ],
    ingreso["razonSocial"  	  ],
    str(ingreso["folio"        	  ]),
    ingreso["fechaEmision" 	  ],
    ingreso["fechaRecepcion"	  ],
    str(ingreso["montoExento"  	  ]),
    str(ingreso["montoNeto"    	  ]),
    str(ingreso["montoIvaRecuperable"]),
    str(ingreso["montoTotal"         ]),
    str(ingreso["ivaNoRetenido"      ]), 
    str(ingreso["totalOtrosImpuestos"]),
    str(ingreso["valorOtroImpuesto"  ]),
    str(ingreso["tasaOtroImpuesto"   ]),
    str(ingreso["tipoDocReferencia"  ]),
    str(ingreso["trackId"      	  ]),
    ingreso["referencias"  	  ],
    ingreso["referenciado" 	  ],
    ingreso["reparos"      	  ],
    ingreso["otrosImpuestos"	  ], 
    ingreso["estado"       	  ]
    listaRut.append(lax)
cur.execute("drop table if exists auxdoc;")
cur.execute("create table auxdoc (id serial, rut varchar(15),folio int);")
query = "select * from auxdoc;"
cur.execute(query)
querySelect = cur.fetchall()
for i in range(len(listaRut)):
    existe=False
    if range(len(querySelect))==0:
        cur.execute("insert into auxdoc (rut,folio)values('61002000-3',5617);")
        cur.execute("select * from auxdoc;")
        print(i)
        print("primer insert si la lista no tiene datos")
    elif range(len(querySelect))!=0: 
        print("entramos a la condicion si existe datos en queryselect")
        print(cur.execute("select * from auxdoc;"))
        for j in range(len(querySelect)):
            if listaRut[i]["rutCliente"]!=querySelect[j]["rut"] and listaRut[i]["folio"]!=querySelect[j]["folio"]:
                print("entramos a la condicion si ")
                l.append(listaRut[0]["rutCliente"]+listaRut[0]["folio"])
                print(l)
        existe=True
    if existe:
        print(cur.execute("select * from auxdoc;"))
        print(range(len(querySelect)))
        cur.execute("insert into auxdoc (rut,folio) values('"+str(listaRut[i][3])+"',"+str(listaRut[i][5])+");")
conn.commit()
print ("Records created successfully");
conn.close()