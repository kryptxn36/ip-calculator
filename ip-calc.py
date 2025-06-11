import re
'''
To do:
--------------------------------------------v1--------------------------------------------
[x] - add broadcast address
[x] - add min-max IP addresses
[x] - figure out wtf happened to lists now being stiffly connected between each other :/ 
*it had to do with list being one of the mutable data types in python
[x] - make it possible to calculate a number of hosts with any subnet mask format
[x] - create user input check (formats of IP and subnet mask)
[x] - create try-except blocks
--------------------------------------------v2--------------------------------------------
[ ] - create support for IPv6 format addresses:
    [x] - make mode selection (IPv4 / IPv6)
    [x] - change user input check if the IPv6 mode is selected
    [x] - rewrite a block of code calculating the number of hosts
    [x] - make a subnet mask format conversion from CIDR to a dot-decimal one
    [x] - convert every element from hexadecimal string to a decimal value
    [x] - make proper IPv6 calculation algorithms for:
        [x] - subnet
        [x] - min/max values
    [x] - create support for abbreviated:
        [x] - input
        [x] - output
    [ ] - make an option to switch between abbreviated and unabbreviated output
--------------------------------------------v3--------------------------------------------
[ ] - create GUI
'''
 
 
def toBinary(num):
    return bin(int(num)).replace("0b", "")
 
def ipv4(m):
    s = []
    wildcard = []
    m = int(m)
    for i in range(m):
        s.append('1')
 
    for i in range(32 - m):
        s.append('0')
    
    for i in range(len(s)):
        wildcard.append(s[i])
        
    for i in range(32):
        if wildcard[i] == '1':
            wildcard[i] = '0'
        elif wildcard[i] == '0':
            wildcard[i] = '1'
 
    for i in range(3):
        wildcard = [a + b for a, b in zip(wildcard[::2], wildcard[1::2])]
    
    for i in range(3):
        s = [a + b for a, b in zip(s[::2], s[1::2])]
 
    for i in range(len(s)):
        wildcard[i] = int(wildcard[i], 2)
        s[i] = int(s[i], 2)
    
    n = 32 - int(m)
    mask = list(map(int, s))
    wildcard = list(map(int, wildcard))
    return mask, wildcard, n
 
def ipv6(m):
        s = []
        wildcard = []
        m = int(m)
        
        for i in range(m):
            s.append('1')
        
        for i in range(128 - m):
            s.append('0')
 
        for i in range(len(s)):
            wildcard.append(s[i])
 
        for i in range(128):
            if wildcard[i] == '1':
                wildcard[i] = '0'
            elif wildcard[i] == '0':
                wildcard[i] = '1'
        
        for i in range(4):
            wildcard = [a + b for a, b in zip(wildcard[::2], wildcard[1::2])]
        
        for i in range(4):
            s = [a + b for a, b in zip(s[::2], s[1::2])]
 
        for i in range(len(s)):
            wildcard[i] = int(wildcard[i], 2)
            s[i] = int(s[i], 2)
        mask = list(map(int, s))
        n = 128 - int(m)
        return mask, wildcard, n
 
def abbreviatedIn(addr):
    zeros = 8 - addr.count(":")
    if addr[-1] == ':':
        addr += '0'
    addr = addr.split(":")
    addr[addr.index(""):addr.index("")] = ['0'] * zeros
    addr.remove('')
    for i in range(8):
        if addr[i] == '':
            addr[i] = '0'
        else:
            continue
    return addr
 
def abbreviatedOut(addr):
    index1 = None
    index2 = None
    counter1 = 0
    counter2 = 0
    for hxt in addr:
        if hxt == '0':
            if not index1:
                index1 = addr.index(hxt)
            counter1 += 1
            if index1 + counter1 < 8 and addr[index1 + counter1] != '0':
                break
            
 
    revAddr = list(reversed(addr))
    for hxt in revAddr:
        if hxt == '0':
            if not index2:
                index2 = revAddr.index(hxt)
            counter2 += 1
            if index2 + counter2 < 8 and revAddr[index2 + counter2] != '0':
                break
 
    if counter2 > counter1:
        for i in range(counter2):
            revAddr.pop(index2)
        revAddr.insert(index2, '')
        return list(reversed(revAddr))
 
    elif counter1 >= counter2:
        for i in range(counter1):
            addr.pop(index1)
        addr.insert(index1, '')
        return addr

     

def main():
    format = False
    while format == False:
        try:
            mode = int(input("[1] IPv4 / [2] IPv6: "))
            if mode == 1 or mode == 2:
                format = True
            else:
                print('Incorrect option!')
        except: print('Incorrect option!')
        
    format = False
    while format == False:
        ip = input("IP: ")
        if mode == 1:
            if re.search(r'^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$', ip) != None:
                ip = ip.split(".")
                format = True
            else: print("Incorrect IPv4 address format!")
        else:
            if re.search(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))', ip) != None:
                if [ip][0:1] == ['', ':'] or [ip][-1:-2] == [':', ''] or '::' in ip:
                    ip = abbreviatedIn(ip)
                else:
                    ip =ip.split(':')
                format = True
            else: print("Incorrect IPv6 address format!")
 
    format = False
    while format == False:
        try:
            mask = input("Subnet mask: ")
            if mode == 1:
                if "." in mask:
                    if re.search(r'^(((255\.){3}(255|254|252|248|240|224|192|128+))|((255\.){2}(255|254|252|248|240|224|192|128|0+)\.0)|((255\.)(255|254|252|248|240|224|192|128|0+)(\.0+){2})|((255|254|252|248|240|224|192|128|0+)(\.0+){3}))$', mask) != None:
                        mask = mask.split(".")
                        mask = str(list(map(toBinary, mask)))
                        mask = mask.count("1")
                        n = ipv4(mask)[2]
                        wildcard = ipv4(mask)[1]
                        mask = ipv4(mask)[0]
                        format = True
                elif int(mask) in range(33):
                    n = ipv4(mask)[2]
                    wildcard = ipv4(mask)[1]
                    mask = ipv4(mask)[0]
                    format = True
                    
            else:
                if int(mask) in range(129):
                    n = ipv6(mask)[2]
                    wildcard = ipv6(mask)[1]
                    mask = ipv6(mask)[0]
                    format = True
        except:
            print('Incorrect subnet mask format!')
    
    if mode == 1:
        ip = list(map(int, ip))
    else:
        ip = [int(x, 16) for x in ip]
   
    network = [a & b for a, b in zip(ip, mask)]
    broadcast = [a | b for a, b in zip(ip, wildcard)]
    
    minBuffer = []
    maxBuffer = []
    if mode == 1:
        network = list(map(int, network))
        for i in range(4):
            minBuffer.append(network[i])
            maxBuffer.append(broadcast[i])
        maxBuffer[-1] = maxBuffer[-1] - 1
        minBuffer[-1] = network[-1] + 1
        hosts = 2 ** n - 2
    else:
        ip = list(map(hex, ip))
        network = list(map(hex, network))
        broadcast = list(map(hex, broadcast))
        for i in range(8):
            minBuffer.append(network[i])
            maxBuffer.append(broadcast[i])
        maxBuffer[-1] = maxBuffer[-1]
        minBuffer[-1] = network[-1]
        hosts = 2 ** n
    
    minAddr = list(map(str, minBuffer))
    maxAddr = list(map(str, maxBuffer))
    #ip = abbreviatedOut(':'.join(ip).replace('0x', ''))
    if mode == 1: 
        ip = list(map(str, ip))
        network = list(map(str, network))
        wildcard = list(map(str, wildcard))
        broadcast = list(map(str, broadcast))
    elif mode == 2:
        wildcard = list(map(hex, wildcard))
        for i in range(8):
            ip[i] = ip[i].replace('0x', '')
            network[i] = network[i].replace('0x', '')
            minAddr[i] = minAddr[i].replace('0x', '')
            maxAddr[i] = maxAddr[i].replace('0x', '')
            wildcard[i] = wildcard[i].replace('0x', '')
        ip = abbreviatedOut(ip)
        network = abbreviatedOut(network)
        minAddr = abbreviatedOut(minAddr)
        maxAddr = abbreviatedOut(maxAddr)
        wildcard = abbreviatedOut(wildcard)
     
    if mode == 1:
        print(f"\n\
    ----SUMMARY----\n\
-Host IP: {'.'.join(ip)} \n\
-Subnet: {'.'.join(network)}\n\
-Number of usable hosts: {hosts}\n\
-Wildcard: {'.'.join(wildcard)}\n\
-Broadcast address: {'.'.join(broadcast)}\n\
-Min host address: {'.'.join(minAddr)}\n\
-Max host address: {'.'.join(maxAddr)}")
    else:
        print(f"\n\
    ----SUMMARY----\n\
-Host IP: {':'.join(ip).replace('0x', '')} \n\
-Subnet: {':'.join(network).replace('0x', '')}\n\
-Number of usable hosts: {hosts}\n\
-Wildcard: {':'.join(wildcard).replace('0x', '')}\n\
-Min host address: {':'.join(minAddr).replace('0x', '')}\n\
-Max host address: {':'.join(maxAddr).replace('0x', '')}")
 
    choice = input("[r]estart, [E]xit: ")
    if choice == 'r' or choice == 'R':
        main()
    else:
        print("Exiting...")
        exit()
 
if __name__ == "__main__":
    main()
