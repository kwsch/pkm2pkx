# 5th Gen to 6th Gen
from __future__ import with_statement

print "5th Gen .pkm to 6th Gen .pkx\nBy Kaphotics.\n"
import os,sys
from array import array
from datetime import date
from tables import spec_abil,movepp,pokestats,lvlexp

def getsum(pkx):
    ar = array('H')
    ar.fromstring(pkx)
    sum = 0
    for val in ar:
        sum += val

    return chr(sum & 0xff) + chr((sum >> 8) & 0xff)

def datemet():
    val = date.today()
    return chr(val.year - 2000) + chr(val.month) + chr(val.day)

def __level(pkm):
	dex = ord(pkm[8]) + (ord(pkm[9]) << 8) # Decimal Reference
	exp = ord(pkm[0x10]) + (ord(pkm[0x11]) << 8) + (ord(pkm[0x12]) << 16)
	
	exptype = pokestats.get(dex)[0]
	for i in xrange(100):
		xpneeded = lvlexp.get(i + 1)[exptype]
		if xpneeded > exp:
			return i
	return 100

def convertname(n):
    bytes = array('B')
    bytes.fromstring(n)
    converted = ''

    for val in bytes:
        if val == 0xff:	# Stop Without Terminators
            break
        converted += chr(val)

    return converted
	
def extendname(n):
	trash='\x00' * 24
	if len(n) < 24:
		n += trash[len(n):]
	return n
	
def makepkx(pkm):
    # Deconstructing PKM File for Access
	
	# Unencrypted Bytes
	pid      = pkm[0x0:0x4]
	# unused = pkm[0x4:0x6]
	checksum = pkm[0x6:0x8]
	
	# Block A
	species  = pkm[0x8:0xA]
	item     = pkm[0xA:0xC]
	tr_id    = pkm[0xC:0xE]
	se_id    = pkm[0xE:0x10]
	exp      = pkm[0x10:0x14]
	friend   = pkm[0x14]
	ability  = pkm[0x15]
	markings = pkm[0x16]
	language = pkm[0x17]
	hp_ev    = pkm[0x18]
	atk_ev   = pkm[0x19]
	def_ev   = pkm[0x1A]
	spe_ev   = pkm[0x1B]
	spa_ev   = pkm[0x1C]
	spd_ev   = pkm[0x1D]
	cool_cv  = pkm[0x1E]
	beau_cv  = pkm[0x1F]
	cute_cv  = pkm[0x20]
	smrt_cv  = pkm[0x21]
	tuff_cv  = pkm[0x22]
	shen_cv  = pkm[0x23]
	sinnoh1  = pkm[0x24:0x26]
	unovar1  = pkm[0x26:0x28]
	
	# Block B
	move_1   = pkm[0x28:0x2A]
	move_2   = pkm[0x2A:0x2C]
	move_3   = pkm[0x2C:0x2E]
	move_4   = pkm[0x2E:0x30]
	move_1_pp= pkm[0x30]
	move_2_pp= pkm[0x31]
	move_3_pp= pkm[0x32]
	move_4_pp= pkm[0x33]
	move_1_pu= pkm[0x34]
	move_2_pu= pkm[0x35]
	move_3_pu= pkm[0x36]
	move_4_pu= pkm[0x37]
	iv_block = pkm[0x38:0x3C]
	hoennr1  = pkm[0x3C:0x3E]
	hoennr2  = pkm[0x3E:0x40]
	fegforme = pkm[0x40]
	nature   = pkm[0x41]
	dwflag   = pkm[0x42]
	# unused = pkm[0x43]
	# unused = pkm[0x44:47]
	
	# Block C
	nickname = pkm[0x48:0x5E]
	# unused = pkm[0x5E]
	game     = pkm[0x5F]
	sinnohr3 = pkm[0x60:0x62]
	sinnohr4 = pkm[0x62:0x64]
	# unused = pkm[0x64:0x68]
	
	# Block D
	otname   = pkm[0x68:0x78]
	eggdate  = pkm[0x78:0x7B]
	metdate  = pkm[0x7B:0x7E]
	eggloc   = pkm[0x7E:0x80]
	metloc   = pkm[0x80:0x82]
	pokerus  = pkm[0x82]
	ball     = pkm[0x83]
	metlvlotg= pkm[0x84]
	enctype  = pkm[0x85]
	# unused = pkm[0x86]
	# fame   = pkm[0x87]
	
	# PKX Block A
	pkx_a = species + item + tr_id + se_id + exp + ability
	
	dex = ord(pkm[8]) + (ord(pkm[9]) << 8) # Decimal Reference
	
	# Determine Ability Number
	if ord(dwflag) > 1:		# Has DW Ability
		pkx_a += '\x04'		
	elif ord(game) < 20: 	# Originates from Gen 3/4
		if (spec_abil.get(dex)[1] == 0) or (pid[0] & 1 == 0): 
			# Has Ability 0
			pkx_a += '\x00'
		else:
			# Has Ability 1
			pkx_a += '\x01'
	else:					# Originates from Gen 5
		if (spec_abil.get(dex)[1] == 0) or (pid[2] & 1 == 0): 
			# Has Ability 0
			pkx_a += '\x00'
		else:
			# Has Ability 1
			pkx_a += '\x01'
			
	pkx_a += '\x00\x00' 	# Unknown
	pkx_a += pid			
	pkx_a += nature
	pkx_a += fegforme
	pkx_a += hp_ev
	pkx_a += atk_ev
	pkx_a += def_ev
	pkx_a += spe_ev
	pkx_a += spa_ev
	pkx_a += spd_ev
	pkx_a += '\x00\x00\x00\x00\x00\x00\x00'	# Unknown x24-x2A
	pkx_a += pokerus
	pkx_a += '\x00\x00\x00\x00' 			# Unknown x2C-x2F
	pkx_a += '\x00\x00\x00\x00'				# Kalos Ribbons
	pkx_a += '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	
	# PKX Block B
	pkx_b = extendname(convertname(nickname)) 
	pkx_b += '\x00\x00'
	pkx_b += move_1 + move_2 + move_3 + move_4
	
	# Get Actual PP
	pp1 = chr((movepp.get(ord(pkm[0x28]) + (ord(pkm[0x29]) << 8))))
	pp2 = chr((movepp.get(ord(pkm[0x2A]) + (ord(pkm[0x2B]) << 8))))
	pp3 = chr((movepp.get(ord(pkm[0x2C]) + (ord(pkm[0x2D]) << 8))))
	pp4 = chr((movepp.get(ord(pkm[0x2E]) + (ord(pkm[0x2F]) << 8))))
	
	pkx_b += pp1 + pp2 + pp3 + pp4
	pkx_b += move_1_pu + move_2_pu + move_3_pu + move_4_pu
	
	# Moves At Hatching
	pkx_b += '\x00' * 8 # Assuming Nothing
	pkx_b += '\x00' * 2 # Unknown
	pkx_b += iv_block
	
	# PKX Block C
	pkx_c = '\x00' * 56 # No Memories! :(
	
	# PKX Block D
	pkx_d = extendname(convertname(otname)) 
	pkx_d += '\x00' * 9 # Unknown
	pkx_d += eggdate + datemet()  # Date Met: Today!
	pkx_d += '\x00' # Unknown
	pkx_d += eggloc + metloc + ball
	
	# Set the Current Level as Met Level, tack on OT-G Bit.
	pkx_d += chr(__level(pkm) + (ord(metlvlotg) & 0x80))
	pkx_d += '\x00' # UU
	pkx_d += game
	pkx_d += '\x00\x00\x00' # Country/Region/3DS Blank
	pkx_d += language
	pkx_d += '\x00' * 4 # Unknown/Unused
	
	pkx = pkx_a + pkx_b + pkx_c + pkx_d 
	# return  pid + '\x00\x00' + '\x00\x00' + pkx
	chksm = getsum(pkx)
	pkx = pid + '\x00\x00' + chksm + pkx
	return pkx
	
def main(inputpk):
	if True == True:
		newpkx = os.path.splitext(inputpk)[0] + ".pkx"
		with open(inputpk,'rb') as f:
			with open(newpkx,'wb') as g:
				g.write(makepkx(f.read()))

def printspacer():
	print "\n/*------------------*/\n"



# Process Drag&Drop
del sys.argv[0]
for item in sys.argv:
	printspacer()
	print "Converting Drag&Drop File:\n%s" % (item)
	main(item)
# Process Manual Input
go=1
while go==1:
	printspacer()
	inputpk = raw_input("Instructions: Drag & Drop PKM File into the window, then press Enter.\nFile: ").replace('"', '')
	print ""
	main(inputpk)
	print ""
	if raw_input("Process another? (y/n): ") != "y":
		go=0
		print ""
		raw_input("Press Enter to Exit.")
		break
