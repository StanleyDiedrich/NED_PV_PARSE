import xml.dom.minidom as xdm
file='/Users/stanislavdidenko/Downloads/ND22-0307762-2/pv13-72-1-b.xml'
with (open(file,'r') as file):
    dom = xdm.parse(file)
    prettyxml= dom.toprettyxml()
with (open('Result.xml','w')as file):
    file.write(prettyxml)