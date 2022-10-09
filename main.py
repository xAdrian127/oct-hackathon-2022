from HealthChain import Doctor, Peer

cooldoc = Doctor()
twodoc = Doctor()
joe = Peer()
mainchain = cooldoc.add_to_chain(r"C:\Users\hatoa\Desktop\Example Medical Record PDF.pdf")
joe.receive_entry(mainchain)
twodoc.receive_entry(mainchain)
print(twodoc.validate(r"C:\Users\hatoa\Desktop\Example Medical Record PDF.pdf", "2022-10-09"))
mainchain = twodoc.add_to_chain(r"C:\Users\hatoa\Desktop\Example Medical Record 1 DOC.docx")
joe.receive_entry(mainchain)
mainchain = twodoc.add_to_chain(r"C:\Users\hatoa\Desktop\Example Medical Record 2 DOC.docx")
joe.receive_entry(mainchain)
[print(x) for x in joe.chain.get().split('}')]
