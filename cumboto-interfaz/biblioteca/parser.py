import re, ConfigParser

f = 'metadatos.conf'

def r_v(d, s):
	for i, j in s.iteritems():
		d = d.replace(i, j)
	return d

def f_p(f):
        lp_cfg=[]
        cfg = open(f, 'r').read() 
        p = cfg.split('\n')
        cfg_p = ConfigParser.RawConfigParser()
	cfp = r""+f+""
	cfg_p.read(cfp)
        print  p
        v = True
	while v == True:
    	    try:
              clsp = p.index ('')
      	      print clsp 
            except ValueError:
              li = -1
              print " no existe el elemento"
              v= False
            if clsp > 0:
               clsp = p.remove ('')   
               print " existe elemento"

        print p      
        for pmt  in range (len(p)):
            if pmt == 0:
                clh = {'[':'',']':''}
                dh = r_v(p[0], clh)
            if pmt > 0:
                cl = {':':'','=':''}
                d = r_v(p[pmt], cl)
                c= d.split()
                e = cfg_p.get(dh, c[0])
                lp_cfg.append(c[0]+' : '+e)
        return lp_cfg        
       
md = f_p(f)

for cf in md:
  print cf
