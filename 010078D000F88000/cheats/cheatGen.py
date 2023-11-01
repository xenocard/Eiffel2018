import sys
sys.path.insert(1,'..\__python__') 
from cheatLib import *

################################ START ######################################

# Game Name in English, and then secondary Language, don't ask for emulator
Init('DRAGON BALL XENOVERSE 2' , '七龍珠 異戰2', False)

playerAddr=RegCodeK()

AddCheat('Protect only 1 player','只保護玩家',1)
Hack(playerAddr,1,False)

AddCheat('Protect only 1 player and 1 team-mate','保護玩家及1位隊友',2)
Hack(playerAddr,2,False)

AddCheat('Protect only 1 player and 2 team-mates','保護玩家及2位隊友',2)
Hack(playerAddr,3,False)

AddCheat('Protect only 1 player and 3 team-mates','保護玩家及3位隊友',2)
Hack(playerAddr,4,False)

AddCheat('Inf Ki','無限氣')
addr=AOB('01 78 21 1E 08 20 20 1E E9 03 27 1E')
CodeCave(addr, ['LDR W8, [X19,#0x40]', 'LDR W0, %d-{here}'%playerAddr, 'CMP W8,W0', 'BGE .+12', 'FMAXNM S0, S0, S1', 'STR S0, %s'%print_operand(addr-8,1), 'FMINNM S1, S0, S1', 'RET'])


AddCheat('Inf Health','無限生命')
addr=AOB('00 18 21 1E ? ? ? ? 41 ? ? BD 68 72 40 B9')
CodeCave(addr, ['LDR W8, [X19,#0x40]', 'LDR W0, %d-{here}'%playerAddr, 'CMP W8,W0', 'BGE .+12',  'FMOV S0, S1', 'STR S0, %s'%print_operand(addr-8,1), 'FDIV S0, S0, S1', 'RET'])


AddCheat('Inf Stamina','無限精力')
addr=AOB3('6A 42 41 39','60 ? 01 BD')
CodeCave(addr, ['LDR W8, [X19,#0x40]', 'LDR W0, %d-{here}'%playerAddr, 'CMP W8,W0', 'BGE .+8', 'FMOV S0, S1', GetDword(addr), 'RET'])


AddCheat('Damage multiplier (2.5x)','攻擊傷害倍率 (2.5x)')
# addr=(AOB3('09 20 90 52 29 00 A0 72 08 69 69 B8 1F 1D 00 71',0x34))
addr=(AOB3('09 03 40 F9 1F 15 00 71','E0 09 2E 1E'))
register=print_operand(addr,0)
CodeCave(addr, [GetDword(addr), 'LDR W8, [X20,#0x40]', 'LDR W0, %d-{here}'%playerAddr, 'CMP W8,W0', 'BGE .+12', 'FMOV S1, #2.5', 'FMUL %s, %s, S1'%(register,register), 'RET'])


savedata=[GetQword(GetADRP(AOB('08 ? ? F9 F3 03 00 AA 00 01 40 F9 14 00 80 12 F5 03 01 2A')))]
# savedata=0x22BF6E0
# slot = [0x22BF6E0] + [0x4C]
# [0x22BF6E0] + [ 0xE790 * slot + 0xDF88 + 0xF4 + 0x68 * idx + 0x4] 
addr=AOB('08 ? ? F9 F3 03 00 AA 00 01 40 F9 14 00 80 12 F5 03 01 2A')
save=[GetQword(GetADRP(addr))]
slotOffset=idc.get_operand_value(AOB2(AOB2(addr,0x18,'? ? ? ? E1 03 00 2A'),0),1)+8
addr2=AOB2(addr,0x18,'? ? ? 52 28 4C 28 9B')
offset1=idc.get_operand_value(addr2,1)
offset2=idc.get_operand_value(addr2+8,1)+0xF8

AddCheat('Preset 1','自訂欄 1 -> 孫悟空在Z篇最後的道服')
AddCheatCode(
    PointerCodeHeader(savedata,'D') +
    PointerCodeAddOffset([slotOffset],'D',4) +
    PointerCodeArithmetic('and','D','D',0xFFFFFFFF) +
    PointerCodeArithmetic('*','D','D',offset1,4) +
    PointerCodeHeader(savedata,'F') +
    PointerCodeArithmetic('+','F','F',offset2+0x68*1) +
    PointerCodeWrite(8, 0x13C, 0x13C, 'F', True, True) +
    PointerCodeWrite(8, 0x13C, 0x13C, 'F', True, True) +
    PointerCodeWrite(8, 0x8A, 0x98, 'F', True, True) +
    PointerCodeWrite(4, 0x0FFFFFFF, None, 'F', True, False)
    )

AddCheat('Preset 2','自訂欄 2 -> SSGSS悟基塔服裝')
AddCheatCode(
    PointerCodeHeader(savedata,'D') +
    PointerCodeAddOffset([slotOffset],'D',4) +
    PointerCodeArithmetic('and','D','D',0xFFFFFFFF) +
    PointerCodeArithmetic('*','D','D',offset1) +
    PointerCodeHeader(savedata,'F') +
    PointerCodeArithmetic('+','F','F',offset2+0x68*2) +
    PointerCodeWrite(8, 0x132, 0x132, 'F', True, True) +
    PointerCodeWrite(8, 0x132, 0x132, 'F', True, True) +
    PointerCodeWrite(8, 0x40, 0x98, 'F', True, True) +
    PointerCodeWrite(4, 0x0FFFFFFF, None, 'F', True, False)
    )

AddCheat('Preset 3','自訂欄 3 -> 布羅利 (全力超級賽亞人) 服裝')
AddCheatCode(
    PointerCodeHeader(savedata,'D') +
    PointerCodeAddOffset([slotOffset],'D',4) +
    PointerCodeArithmetic('and','D','D',0xFFFFFFFF) +
    PointerCodeArithmetic('*','D','D',offset1) +
    PointerCodeHeader(savedata,'F') +
    PointerCodeArithmetic('+','F','F',offset2+0x68*3) +
    PointerCodeWrite(8, 0x131, 0x131, 'F', True, True) +
    PointerCodeWrite(8, 0x131, 0x131, 'F', True, True) +
    PointerCodeWrite(8, 0x8D, 0x98, 'F', True, True) + 
    PointerCodeWrite(4, 0x0FFFFFFF, None, 'F', True, False)
    )

AddCheat('Preset 4','自訂欄 4 -> 全王服裝')
AddCheatCode(
    PointerCodeHeader(savedata,'D') +
    PointerCodeAddOffset([slotOffset],'D',4) +
    PointerCodeArithmetic('and','D','D',0xFFFFFFFF) +
    PointerCodeArithmetic('*','D','D',offset1) +
    PointerCodeHeader(savedata,'F') +
    PointerCodeArithmetic('+','F','F',offset2+0x68*4) +
    PointerCodeWrite(8, 0x123, 0x123, 'F', True, True) +
    PointerCodeWrite(8, 0x123, 0x123, 'F', True, True) +
    PointerCodeWrite(8, 0x74, 0x98, 'F', True, True) +
    PointerCodeWrite(4, 0x0FFFFFFF, None, 'F', True, False)
    )
    
AddCheat('Preset 5','自訂欄 5 -> 終極賽魯的服裝')
AddCheatCode(
    PointerCodeHeader(savedata,'D') +
    PointerCodeAddOffset([slotOffset],'D',4) +
    PointerCodeArithmetic('and','D','D',0xFFFFFFFF) +
    PointerCodeArithmetic('*','D','D',offset1) +
    PointerCodeHeader(savedata,'F') +
    PointerCodeArithmetic('+','F','F',offset2+0x68*5) +
    PointerCodeWrite(8, 0x153, 0x153, 'F', True, True) +
    PointerCodeWrite(8, 0x153, 0x153, 'F', True, True) +
    PointerCodeWrite(8, 0x65, 0x98, 'F', True, True) +
    PointerCodeWrite(4, 0x0FFFFFFF, None, 'F', True, False)
    )

AddCheat('Preset 6','自訂欄 6 -> 超級賽亞人4服裝')
AddCheatCode(
    PointerCodeHeader(savedata,'D') +
    PointerCodeAddOffset([slotOffset],'D',4) +
    PointerCodeArithmetic('and','D','D',0xFFFFFFFF) +
    PointerCodeArithmetic('*','D','D',offset1) +
    PointerCodeHeader(savedata,'F') +
    PointerCodeArithmetic('+','F','F',offset2+0x68*6) +
    PointerCodeWrite(8, 0x11D, 0x11D, 'F', True, True) +
    PointerCodeWrite(8, 0x11D, 0x11D, 'F', True, True) +
    PointerCodeWrite(8, 0x7E, 0x98, 'F', True, True) +
    PointerCodeWrite(4, 0x0FFFFFFF, None, 'F', True, False)
    )

AddCheat('Preset 7','自訂欄 7 -> 金色龜仙流服')
AddCheatCode(
    PointerCodeHeader(savedata,'D') +
    PointerCodeAddOffset([slotOffset],'D',4) +
    PointerCodeArithmetic('and','D','D',0xFFFFFFFF) +
    PointerCodeArithmetic('*','D','D',offset1) +
    PointerCodeHeader(savedata,'F') +
    PointerCodeArithmetic('+','F','F',offset2+0x68*7) +
    PointerCodeWrite(8, 0x11B, 0x11B, 'F', True, True) +
    PointerCodeWrite(8, 0x11B, 0x11B, 'F', True, True) +
    PointerCodeWrite(8, 0x7B, 0x98, 'F', True, True) +
    PointerCodeWrite(4, 0x0FFFFFFF, None, 'F', True, False)
    )


AddCheat('Max Zeni','索尼 最大')
Hack(AOB2('? ? ? ? 00 10 2E 1E 60 02 02 B9',0,'61 00 00 54'), ['MOV W0, #0xC9FF', 'MOVK W0, #0x3B9A,LSL#16'])


AddCheat('Max TP', '最大 TP')
Hack('89 01 00 4A', ['MOV W0, #0xC9FF', 'MOVK W0, #0x3B9A,LSL#16'])


AddCheat('Level 99', '等級 99')
Hack(AOB2('? ? ? ? 61 B2 40 B9 60 B6 00 B9',0,'00 01 00 4A'), 'MOV W0,#99')


AddCheat('100,000,000 Total EXP', '一億 總經驗值')
Hack(AOB2('? ? ? ? C8 02 00 4B E0 03 13 AA',0,'61 00 00 54'), ['MOV W0, #0xE100','MOVK W0, #0x5F5,LSL#16'])


AddCheat('9,999 Attribute Points', '9999 強化能力點數')
Hack(AOB2('? ? ? ? 60 D2 01 B9 E0 03 14 AA',0,'00 01 00 4A'), 'MOV W0,#9999')


AddCheat('Max All Attributes', '所有屬性 MAX')
Hack(AOB2('? ? ? ? 60 D6 01 B9 E0 03 14 AA',0,'00 01 00 4A'), 'MOV W0,#127')
Hack(AOB2('? ? ? ? 60 DA 01 B9 E0 03 14 AA',0,'00 01 00 4A'), 'MOV W0,#127')
Hack(AOB2('? ? ? ? 60 DE 01 B9 E0 03 14 AA',0,'00 01 00 4A'), 'MOV W0,#127')
Hack(AOB2('? ? ? ? 60 E2 01 B9 E0 03 14 AA',0,'00 01 00 4A'), 'MOV W0,#127')
Hack(AOB2('? ? ? ? 60 E6 01 B9 E0 03 14 AA',0,'00 01 00 4A'), 'MOV W0,#127')
Hack(AOB2('? ? ? ? 60 EA 01 B9 FD 7B 41 A9 F4 4F C2 A8',0,'00 01 00 4A'), 'MOV W0,#127')


AddCheat('Instructors\' Friendship Max after talk','跟導師交談後,友好度最大')
Hack('08 B1 89 1A E0 03 15 AA', 'MOV W8, W9')

AddCheat('Movement Speed 4x (Hold ZL)', '移動速度 4x (長按ZL)')
Hack('A1 02 40 BD 83 3A 47 B9', 'FMOV S1, #0.125', useButton='ZL')

AddCheatCode('\n[Credit to @patjenova https://gbatemp.net/threads/cheat-codes-ams-and-sx-os-add-and-request.520293/post-9494090]\n20000000')

################################# END #######################################