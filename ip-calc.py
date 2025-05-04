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
[ ] - create support for IPv6 format addresses
[ ] - create GUI
'''

def main():
    global ip
    global mask
    global wildcard
    
    def toBinary(num):
        return bin(int(num)).replace("0b", "")

    def decimalPointMask(m):
        '''
        A neat function that converts a mask in any given format to a decimal-point one
        '''
        global mask
        global n
        global wildcard
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
    
    format = False
    while format == False:
        ip = input("IP: ")
        if re.search(r'^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$', ip) != None:
            ip = ip.split(".")
            format = True
        else: print('Incorrect IPv4 address format!')
    
    format = False
    while format == False:
        try:
            mask = input("Subnet mask: ")
            if "." in mask:
                if re.search(r'^(((255\.){3}(255|254|252|248|240|224|192|128+))|((255\.){2}(255|254|252|248|240|224|192|128|0+)\.0)|((255\.)(255|254|252|248|240|224|192|128|0+)(\.0+){2})|((255|254|252|248|240|224|192|128|0+)(\.0+){3}))$', mask) != None:
                    mask = mask.split(".")
                    mask = str(list(map(toBinary, mask)))
                    mask = mask.count("1")
                    decimalPointMask(mask)
                    format = True
            elif int(mask) in range(33):
                    decimalPointMask(mask)
                    format = True
        except:
            print('Incorrect subnet mask format!')
            
    ip = list(map(int, ip))

    network = [a & b for a, b in zip(ip, mask)]
    broadcast = [a | b for a, b in zip(ip, wildcard)]

    maxBuffer = []
    for i in range(4):
        maxBuffer.append(broadcast[i])

    maxBuffer[-1] = maxBuffer[-1] - 1
    maxAddr = list(map(str, maxBuffer))

    minBuffer = []
    for i in range(4):
        minBuffer.append(network[i])

    minBuffer[-1] = network[-1] + 1
    minAddr = list(map(str, minBuffer))

    ip = list(map(str, ip))
    network = list(map(str, network))
    broadcast = list(map(str, broadcast))
    wildcard = list(map(str, wildcard))

    hosts = 2 ** n - 2

    print(f"\n\
    ----SUMMARY----\n\
-Host IP: {'.'.join(ip)} \n\
-Subnet: {'.'.join(network)}\n\
-Number of usable hosts: {hosts}\n\
-Wildcard: {'.'.join(wildcard)}\n\
-Broadcast address: {'.'.join(broadcast)}\n\
-Min host address: {'.'.join(minAddr)}\n\
-Max host address: {'.'.join(maxAddr)}")
    
    choice = input("[r]estart, [E]xit: ")
    if choice == 'r' or choice == 'R':
        main()
    else:
        print("Exiting...")
        exit()

if __name__ == "__main__":
    main()