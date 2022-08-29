import argparse
import os

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-i', '--new_sv', type=str,
                    help='new symvers to parse')
parser.add_argument('-o', '--sv_store', type=str, default="svstore.txt",
                    help='symvers store to append to, default: svstore.txt')
parser.add_argument('-a', dest='append_sv', action='store_true',
                    help='append to the input sv_store')
parser.add_argument('--header', type=str,
                    help='header file to generate')
                    
args = parser.parse_args()

# 0xa60650f5	security_inode_copy_up	vmlinux	EXPORT_SYMBOL

header_template = """
#ifndef KCRC_STORE_H
#define KCRC_STORE_H

#include <map>
#include <string>

typedef enum
{{
    NONGPL_SYM=1,
    GPL_SYM
}} gpl_symtype;

std::map<std::string, gpl_symtype> ksym_map = 
{{
{}
}};

#endif
"""

def parse_symvers(symvers_name, symvers_store):
    f = open(symvers_name, 'r')
    g = f.readlines()
    f.close()

    if os.path.isfile(symvers_name) == False:
        print("symvers {} not found".format(symvers_name))
        return symvers_store

    for ksym in g:
        ksym = ksym.replace('\n', '')
        liksplit = ksym.split('\t')
        # assume that its over, bail
        if len(liksplit) != 4:
            break
        ksymstr = liksplit[1]
        gpl = liksplit[3]
        if gpl == "EXPORT_SYMBOL":
            gpl = "NONGPL_SYM"
        else:
            gpl = "GPL_SYM"
        symvers_store[ksymstr] = gpl
    return symvers_store

def parse_symstore(symstore_name):
    symvers_new = {}

    if os.path.isfile(symstore_name) == False:
        print("symstore {} not found, gonna be creating a new one".format(symstore_name))
        return symvers_new

    f = open(symstore_name, 'r')
    g = f.readlines()
    f.close()

    for ksym in g:
        ksym = ksym.replace('\n', '')
        liksplit = ksym.split('\t')
        # assume that its over, bail
        if len(liksplit) != 2:
            break
        ksymstr = liksplit[0]
        gpl = liksplit[1]
        symvers_new[ksymstr] = gpl
    return symvers_new

def append_sv(symstore_name, symvers_store):
    f = open(symstore_name, 'w')
    for i in symvers_store:
        f.write("{}\t{}\n".format(i, symvers_store[i]))
    f.close()

def gen_header(header_name, sv_store):
    f = open(header_name, 'w')
    sw_store_arrblock = ''
    for i in sv_store:
        ksym_tmp = '\t{{ \"{}\", {} }},\n'.format(i, sv_store[i])
        sw_store_arrblock += ksym_tmp
    sw_store_sum = header_template.format(sw_store_arrblock)
    f.write(sw_store_sum)
    f.close()    

def main():

    sv_store = {}

    if args.sv_store != None:
        sv_store = parse_symstore(args.sv_store)
    if args.new_sv != None:
        sv_store = parse_symvers(args.new_sv, sv_store)
    if (args.append_sv == True) and (args.sv_store != None):
        append_sv(args.sv_store, sv_store)
    if args.header != None:
        gen_header(args.header, sv_store)

if __name__ == "__main__":
    main()