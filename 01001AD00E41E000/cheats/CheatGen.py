# This Script is Programmed by Eiffel2018
# Works in IDA PRO v7.5 up 
# Requirement: Python 3.9.x (with idapyswitch) and Keystone 
# Operate with a clean NSO (or main.elf) or GDB connected with segment defined by markRegions64.py

import idc
import ida_search
from keystone import *

patch = False # set to True if you want to apply the cheat code to IDA memory
CodeStart = ida_segment.get_segm_by_name('.text').start_ea
CodeEnd = ida_segment.get_segm_by_name('.rodata').start_ea
DataStart = ida_segment.get_segm_by_name('.data').start_ea
DataEnd = ida_segment.get_segm_by_name('.prgend').start_ea

if patch:
    idc.set_name(CodeStart, 'CodeStart', idc.SN_AUTO)
    idc.set_name(CodeEnd, 'CodeEnd', idc.SN_AUTO)
    idc.set_name(DataStart, 'DataStart', idc.SN_AUTO)
    idc.set_name(DataEnd, 'DataEnd', idc.SN_AUTO)

ida_kernwin.activate_widget(ida_kernwin.find_widget("Output window"), True);
ida_kernwin.process_ui_action("msglist:Clear");

def isFound(opAddr):
    return opAddr != BADADDR
def Addr2DWord(opAddr):
    return "{:08X}".format(opAddr & 0xFFFFFFFF)
def Value2DWord(value):
    if type(value) is str: value=int(value.replace(' ',''), 16)
    return "{:08X}".format(value & 0xFFFFFFFF)
def Value2QWord(value):
    if type(value) is str: value=int(value.replace(' ',''), 16)
    return "{:08X} {:08X}".format(value // 0x100000000, value & 0xFFFFFFFF)
def Float2DWord(f):
    return struct.unpack('<I', struct.pack('<f', f))[0]
def GetBytes(length,opAddr):
    return {1:ida_bytes.get_original_byte(opAddr), 2:ida_bytes.get_original_word(opAddr), 4:ida_bytes.get_original_dword(opAddr), 8:ida_bytes.get_original_dword(opAddr)}[length]
def PatchBytes(length,opAddr,value):
    if type(value) is str: value=int(value.replace(' ',''), 16)
    if (length==1):
        ida_bytes.patch_byte(opAddr,value)
    elif (length==2):
        ida_bytes.patch_word(opAddr,value)
    elif (length==4):
        ida_bytes.patch_dword(opAddr,value)
    elif (length==8):
        ida_bytes.patch_qword(opAddr,value)
    else:
        print('Error in PatchBytes({},{},{})',length,opAddr,value) 
def CheatCode(length,opAddr,value,isPatch=patch):
    if isPatch: PatchBytes(length,opAddr,value)
    return '0{}0E0000 {} {}'.format(length,Addr2DWord(opAddr),Value2DWord(value) if length<=4 else Value2QWord(value))
def RestoreCode(length,opAddr):
    return CheatCode(length,opAddr,GetBytes(length,opAddr),False)
def PointerCode(oppsets, length, value): # oppsets use tuples/list with at least 2 element
    if len(oppsets)<2: return 'Error with PointerCode'
    else:
        code = '580{}0000 {:08X}'.format(TM,oppsets[0])
        for offset in oppsets[1:-1]: 
            code += '\n580{}1000 {:08X}'.format(TM,offset)
        code += '\n780{}0000 {:08X}'.format(TM,oppsets[-1])
        code += '\n6{:1X}0{}0000 {}'.format(length, TM, Value2QWord(value))
        return code
def ButtonCode(key,code):
    return '8{:07X}\n{}\n20000000'.format(key,code)
def ASM(asm_code):
    ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
    bytecode, cnt = ks.asm(asm_code, as_bytes=True)
    return ''.join(map('{:02X}'.format, reversed(bytecode)))
def GrepAddr(opAddr):
    idc.create_insn(opAddr);idc.create_insn(opAddr+4)
    return idc.get_operand_value(opAddr,1)+idc.get_operand_value(opAddr+4,1)
def PraseADRP(base,target):
    return hex((target&0xFFFFF000)-(base&0xFFFFF000))
def AOB(pattern,searchStart=CodeStart):
    return ida_search.find_binary(searchStart, CodeEnd, pattern, 0, idc.SEARCH_DOWN|idc.SEARCH_NEXT)
def AOB2(pattern,offset,pattern2):
    opAddr=AOB(pattern)
    return AOB(pattern2,idc.get_operand_value(opAddr+offset,0)) if isFound(opAddr) else BADADDR
def AOB3(pattern,pattern2):
    opAddr=AOB(pattern)
    return AOB(pattern2,opAddr+4) if isFound(opAddr) else BADADDR
def allOccur(pattern):
    result=[]
    CheatAddr=AOB(pattern)
    while isFound(CheatAddr):
        result.append(CheatAddr)
        CheatAddr=AOB(pattern,CheatAddr+4)
    return result
def checkUnique(pattern):
    CheatAddr=AOB(pattern)
    return not(isFound(AOB(pattern,CheatAddr))) if isFound(CheatAddr) else None
def getBytesPattern(opAddr):
    return ' '.join('{:02X}'.format(x) for x in ida_bytes.get_bytes(opAddr, 4))
def anaysis(opAddr):
    cmd=idc.print_insn_mnem(opAddr)
    if cmd == 'BL' or cmd == 'B':
        return '? ? ? {:02X}'.format(ida_bytes.get_original_byte(opAddr+3))
    elif cmd == 'ADRP':
        return '? ? ? ?'
    elif 'PAGEOFF' in print_operand(opAddr,1):
        return "{:02X} ? ? {:02X}".format(ida_bytes.get_original_byte(opAddr),ida_bytes.get_original_byte(opAddr+3))
    else:
        return getBytesPattern(opAddr)
def getAOB(opAddr):
    pattern=space=''
    result=False
    funcEnd=idc.find_func_end(opAddr)
    while opAddr<funcEnd and result==False:
        pattern+=space+anaysis(opAddr)
        space=' '
        opAddr+=4
        result=checkUnique(pattern)
    return 'Not found' if result==None else pattern
    

################################ START ######################################

print("[ Megaton Musashi (TID:01001AD00E41E000)]")

DelayOutput = ''
print('\n{Restore Codes}')


CheatName = '#01. Infinite HP/Medicine/Items'
CheatAddr = AOB('08 74 41 39 48 00 00 34 C0 03 5F D6 08 50 40 B9 08 01 01 4B')
if isFound(CheatAddr):
    DelayOutput += '\n\n[' + CheatName + ']'
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('MOV W8, #1'));
    print(RestoreCode(4,CheatAddr))
else:
    print(CheatName+': AOB broken!')
	

CheatName = '#02. Infinite TP and Boost'
CheatAddr = AOB('00 F0 40 39 C0 03 5F D6 1F 20 03 D5 1F 20 03 D5 E9 23 BD 6D F4 4F 01 A9 FD 7B 02 A9 FD 83 00 91')
if isFound(CheatAddr):
    DelayOutput += '\n\n[' + CheatName + ']'
    DelayOutput += '\n' + CheatCode(4,CheatAddr+0x10,ASM('RET'));
    print(RestoreCode(4,CheatAddr+0x10))
else:
    print(CheatName+': AOB broken!')
	

CheatName = '#03. Infinite Ammo'
CheatAddr = AOB('08 74 41 39 88 00 00 35 08 50 40 B9 08 05 00 51')
if isFound(CheatAddr):
    DelayOutput += '\n\n[' + CheatName + ']'
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('MOV W8, #1'));
    print(RestoreCode(4,CheatAddr))
else:
    print(CheatName+': AOB broken!')


CheatName = '#04. 5x EXP'
CheatAddr = AOB2('A1 2E 40 B9 A0 2A 00 B9 E0 03 14 AA E2 03 1F AA',0x10,'F4 03 01 2A F3 03 00 AA')
if isFound(CheatAddr): 
    DelayOutput += '\n\n[' + CheatName + ']'
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('ADD  W20, W1, W1,LSL#2'))
    print(RestoreCode(4,CheatAddr))
else:
    print(CheatName+': AOB broken!')


CheatName = '#05. 5x Money/PP'
CheatAddr = AOB2('A1 46 40 B9 A0 42 00 B9 E0 03 14 AA E2 03 1F AA',0x10,'F3 03 01 2A')
CheatAddr1 = AOB2('61 3A 40 B9 60 36 00 B9 E0 03 18 AA E2 03 1F AA',0x10,'F3 03 01 2A')
if isFound(CheatAddr) and isFound(CheatAddr1): 
    DelayOutput += '\n\n[' + CheatName + ']'
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('ADD W19, W1, W1,LSL#2'))
    print(RestoreCode(4,CheatAddr))

    CheatAddr = CheatAddr1
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('ADD W19, W1, W1,LSL#2'))
    print(RestoreCode(4,CheatAddr))

else:
    print(CheatName+': AOB broken!')
    
    
CheatName = '#06. 5x Items/Materials etc.'
CheatAddrs = allOccur('F3 03 02 2A F4 03 01 2A E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 A8 ? ? 39 ? ? ? ? 08 ? ? F9 00 01 40 F9 08 BC 44 39 88 00 08 36 08 E0 40 B9 48 00 00 35 ? ? ? 97 E0 03 1F AA ? ? ? 97 00 18 40 F9 E1 03 14 2A E2 03 13 2A FD 7B 42 A9 E3 03 1F AA F4 4F 41 A9 F5 07 43 F8 ? ? ? 14')+allOccur('F3 03 02 2A F4 03 01 2A E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 A8 ? ? 39 ? ? ? ? A8 ? ? 39 E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 A8 ? ? 39 ? ? ? ? 08 ? ? F9 00 01 40 F9 08 BC 44 39 88 00 08 36 08 E0 40 B9 48 00 00 35 ? ? ? 97 E0 03 1F AA ? ? ? 97 ? ? ? ? 15 18 40 F9')
CheatAddr1 = AOB('F3 03 02 2A F4 03 01 2A E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 A8 ? ? 39 ? ? ? ? 08 ? ? F9 01 01 40 F9')
CheatAddrs1 = allOccur('F4 03 01 2A F3 03 00 AA E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 A8 ? ? 39 ? ? ? ? 08 ? ? F9 00 01 40 F9 75 ? 40 B9 08 BC 44 39 88 00 08 36 08 E0 40 B9 48 00 00 35 ? ? ? 97 A0 02 14 0B ? ? 80 52')

if len(CheatAddrs)>7 and len(CheatAddrs1)>5 and isFound(CheatAddr1): 
    DelayOutput += '\n\n[' + CheatName + ']'

    for CheatAddr in CheatAddrs:
        DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('ADD W19, W2, W2,LSL#2'))
        print(RestoreCode(4,CheatAddr))

    CheatAddr = CheatAddr1
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('ADD W19, W2, W2,LSL#2'))
    print(RestoreCode(4,CheatAddr))

    for CheatAddr in CheatAddrs1:
        DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('ADD W20, W1, W1,LSL#2'))
        print(RestoreCode(4,CheatAddr))

else:
    print(CheatName+': AOB broken!')


CheatName = '#07. Money/PP never decrease'
CheatAddr = AOB('F3 03 01 2A E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 88 ? ? 39 ? ? ? ? 88 ? ? 39 E8 00 00 37')
CheatAddr1 = AOB('08 ? ? F9 00 01 40 F9 ? ? ? 94 88 02 40 F9 F5 03 00 AA')
CheatAddr2 = AOB('F3 03 01 2A E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 88 ? ? 39 ? ? ? ? ? ? ? ? 88 ? ? 39 B5 ? ? F9 A8 00 00 37 A0 02 40 B9 ? ? ? 97 28 00 80 52 88 ? ? 39 ? ? ? ? D6 ? ? F9 C0 02 40 F9 08 BC 44 39 88 00 08 36 08 E0 40 B9 48 00 00 35 ? ? ? 97 E0 03 1F AA ? ? ? 97 17 0C 40 F9 88 ? ? 39 A8 00 00 37 A0 02 40 B9 ? ? ? 97 28 00 80 52 88 ? ? 39 C0 02 40 F9 08 BC 44 39 88 00 08 36 08 E0 40 B9 48 00 00 35 ? ? ? 97 E0 03 1F AA ? ? ? 97 ? ? ? ? 08 0C 40 F9 29 ? ? F9 18 1D 40 B9')
if isFound(CheatAddr) and isFound(CheatAddr1) and isFound(CheatAddr2): 
    DelayOutput += '\n\n[' + CheatName + ']'
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('MOV W19, WZR'))
    print(RestoreCode(4,CheatAddr))

    CheatAddr = CheatAddr1-8
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('NOP'))
    print(RestoreCode(4,CheatAddr))

    CheatAddr = CheatAddr2
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('MOV W19, WZR'))
    print(RestoreCode(4,CheatAddr))

else:
    print(CheatName+': AOB broken!')

CheatName = '#08. Items/Materials etc. never decrease'
CheatAddrs = allOccur('F3 03 02 2A F4 03 01 2A E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 A8 ? ? 39 ? ? ? ? A8 ? ? 39 E8 00 00 37 ? ? ? ? 08 ? ? F9 00 01 40 B9 ? ? ? 97 28 00 80 52 A8 ? ? 39 ? ? ? ? 08 ? ? F9 00 01 40 F9 08 BC 44 39 88 00 08 36 08 E0 40 B9 48 00 00 35 ? ? ? 97 E0 03 1F AA ? ? ? 97 08 18 40 F9 16 ? ? F9')

if len(CheatAddrs)>7: 
    DelayOutput += '\n\n[' + CheatName + ']'

    for CheatAddr in CheatAddrs:
        DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('MOV W19, WZR'))
        print(RestoreCode(4,CheatAddr))
else:
    print(CheatName+': AOB broken!')

CheatName = '#09. 100% Legendary in Recycle Production'
CheatAddr = AOB('85 01 00 54 34 01 00 37')
CheatAddr1 = AOB('09 F0 A7 52 09 19 00 B9 FD 7B 41 A9')
if isFound(CheatAddr) and isFound(CheatAddr1):
    DelayOutput += '\n\n[' + CheatName + ']'
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('NOP'));
    print(RestoreCode(4,CheatAddr))

    CheatAddr = CheatAddr1
    DelayOutput += '\n' + CheatCode(4,CheatAddr,ASM('MOV  W9, '+hex(Float2DWord(100))));
    print(RestoreCode(4,CheatAddr))
else:
    print(CheatName+': AOB broken!')


print(DelayOutput)
print('\n[Created by Eiffel2018, enjoy!]\n')

################################# END #######################################