from rest_framework.views import APIView
from rest_framework.response import Response
from math import floor
from collections import Counter

class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def dhondt(self, options, seats):
        out = []

        options.sort(key=lambda x: -x['votes'])
        for opt in options:
            out.append({
                **opt,
                'postproc': 0,
            })

        for _ in range(seats):

            control_var = 0

            for opt1, opt2 in zip(out, out[1:]):
                max_value1 = opt1['votes'] / (opt1['postproc'] + 1)
                max_value2 = opt2['votes'] / (opt2['postproc'] + 1)

                if (max_value1 >= max_value2):
                    opt1['postproc'] += 1
                    control_var = 1
                    break

            if (control_var == 0):
                out[-1]['postproc'] += 1
            
        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return Response(out)

    def droop(self, options, seats):
        out = []

        e, r = [], []
        sum_e = 0
        m = sum([opt['votes'] for opt in options])
        q = round(1 + m / (seats + 1))

        for i, opt in enumerate(options):
            ei = floor(opt['votes'] / q)
            ri = opt['votes'] - q*ei
            e.append(ei)
            r.append((ri, i))
            sum_e += ei

        k = seats - sum_e
        r.sort(key = lambda x: -x[0])
        best_r_index = Counter(i for _, i in (r*k)[:k])
        
        for i, opt in enumerate(options):
            out.append({
                **opt,
                'postproc': e[i] + best_r_index[i] if i in best_r_index else e[i],
            })

        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return Response(out)



    def borda(self, options):

        salida = {}
        
        boole = False

        for opcion in options:
            
            if len(opcion['positions']) != 0:

                suma_total_opcion = 0

                for posicion in opcion['positions']:

                    valor = len(options) - posicion + 1
                    suma_total_opcion += valor

                salida[opcion['option']] = suma_total_opcion
                opcion['votes'] = suma_total_opcion

            else:
                salida = {}
                boole = True
                break

        if boole == True:

            for opcion in options:

                opcion['votes'] = 0

        return Response(options)



    def post(self, request):
        """
         * type: IDENTITY | DHONDT | DROOP
         * seats: int (just in case type is DHONDT or DROOP)
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        response = Response({})

        t = request.data.get('type', 'IDENTITY')
        seats = request.data.get('seats', 1)
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            response = self.identity(opts)
        elif t == 'DHONDT':
            response = self.dhondt(opts, seats)
        elif t == 'DROOP':
            response = self.droop(opts, seats)
        

        return response
