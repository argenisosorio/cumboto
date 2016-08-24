from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
import ocumare
#import cumaco.lutheria from tsco


def obt_list(self):
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    lista = octs.obt_serv_md()
    print(lista)
    return self.octs.obt_serv_md()
