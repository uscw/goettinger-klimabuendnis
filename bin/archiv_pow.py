DIR = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/"
IFN = DIR + "config.toml"
OFN = DIR + "content/top/pow.md"

IFD=open(IFN,"r")
OFD=open(OFN,"w")

for line in IFD:
        if len(line.split()) > 0 and line.split()[0].replace("#","") == "sidebar_pow":
            pic_ref = line.split('"')[1]
            pic_title = pic_ref.split("/")[2]
        elif len(line.split()) > 0 and line.split()[0].replace("#","") == "sidebar_pow_description":
            descr = line.split('"')[1]
            OFD.write ( descr + "![" +  pic_title + "](/" + pic_ref + ")\n------------------\n")
