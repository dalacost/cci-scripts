import requests
import sys
from urllib3.contrib import pyopenssl
from OpenSSL import SSL
import ssl, socket
import OpenSSL

MEMO_LIST='AESGENER,AGUAS-A,ANDINA-B,ANTARCHILE,BANMEDICA,BCI,BSANTANDER,CAP,CCU,CENCOSUD,CFMITNIPSA,CHILE,CMPC,COLBUN,CONCHATORO,COPEC,ECL,EMBONOR-B,ENELAM,ENELCHILE,ENELGXCH,ENTEL,FALABELLA,FORUS,IAM,ILC,ITAUCORP,LTM,MASISA,ORO BLANCO,PARAUCO,QUINENCO,RIPLEY,SALFACORP,SECURITY,SK,SM-CHILE B,SMSAAM,SONDA,SQM-B,VAPORES'
DATA_URL= 'http://www.ccbolsa.cl/apps/script/Asp/rutinasAC.asp?Ejecutar=2&nemo='
PORCENTAJE_MINIMO=0.5



if __name__ == '__main__':
#	cert=ssl.get_server_certificate(('www.ccbolsa.cl', 443))
	# OpenSSL
#	x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
#	x509.get_subject().get_components()


	for MEMO in MEMO_LIST.split(","):

		session = requests.session()
		#print(DATA_URL+''+MEMO)
		r = session.get(DATA_URL+''+MEMO)
		r = r.text.replace(".","")
		r = r.replace(",",".")
		grupos = r.split("|")
		valores=grupos[1].split(";")
		valores_volumen=grupos[2].split(";")

		#print("valor actual:"+valores[0])
		#print("Punta Compra:"+valores[1])
		#print("Punta Venta:"+valores[2])
#		print("volumen:"+valores_volumen[0])


		potencial=  round(float(valores[2])*100/float(valores[0])-100,2)

		plus =""
		#esta en su minimo, interesante para ver.
		if valores[0] == valores[1] and valores[1] < valores[2] :
			plus="**"
		#esta en su mini con potencial de subida interesante
		if valores[0] < valores[1] and potencial >= PORCENTAJE_MINIMO:
                        plus="** comprar ahora!"
			if float(valores_volumen[0])==0.0:
				plus=plus+" Pero Volumen 0!! estar atento!"

		#potencial de caida fuerte
		if potencial <= 0 and potencial <= PORCENTAJE_MINIMO*-1:
			 plus="** Vender ahora!"

		print(MEMO+" Potencial:"+str(potencial)+"% "+plus)

