from rest_framework.views import APIView
from rest_framework.response import Response
from math import floor
from collections import Counter
import math
import copy

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
    
    def imperiali(sel, options, seats):
        out = []

        seats_per_quotien = []
        residues = []
        sum_e = 0
        votes = 0
        for option in options:
            votes += option['votes']
        quotient = votes / (seats + 2)

        for i, option, in enumerate(options):
            ei = floor(option['votes']/quotient)
            ri = option['votes'] - quotient * ei
            seats_per_quotien.append(ei)
            residues.append((ri,i))
            sum_e += ei

        free_seats = seats - sum_e
        residues.sort(key = lambda x: -x[0])
        best_r_index = Counter(i for _, i in (residues*free_seats)[:free_seats])
        
        for i, option in enumerate(options):
            out.append({
                **option,
                'postproc': seats_per_quotien[i] + best_r_index[i] if i in best_r_index else seats_per_quotien[i],
            })

        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return Response(out)

    def hare(self, options, seats):
        out = []

        e, r = [], []
        sum_e = 0
        m = sum([opt['votes'] for opt in options])
        q = round(m/seats, 3)

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
    
    def reinforced_imperial(self, options, seats):
        out = []

        seats_quotient = []
        remainder = []
        sum_e = 0
        total_votes = sum([option['votes'] for option in options])
        quotient = total_votes / (seats + 3)

        for num, option in enumerate(options):
            ei = floor(option['votes'] / quotient)
            ri = option['votes'] - quotient*ei
            seats_quotient.append(ei)
            remainder.append((ri, num))
            sum_e += ei

        k = seats - sum_e
        remainder.sort(key = lambda x: -x[0])
        best_r_index = Counter(num for _, num in (remainder*k)[:k])
        
        for num, option in enumerate(options):
            out.append({
                **option,
                'postproc': seats_quotient[num] + best_r_index[num] if num in best_r_index else seats_quotient[num],
            })

        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return Response(out)

    def hagenbach_bischoff(sel, options, seats):
        out = []

        seats_per_quotien = []
        residues = []
        sum_e = 0
        votes = 0
        for option in options:
            votes += option['votes']
        quotient = votes / (seats + 1)

        for i, option, in enumerate(options):
            ei = floor(option['votes']/quotient)
            ri = option['votes'] - quotient * ei
            seats_per_quotien.append(ei)
            residues.append((ri,i))
            sum_e += ei

        free_seats = seats - sum_e
        residues.sort(key = lambda x: -x[0])
        best_r_index = Counter(i for _, i in (residues*free_seats)[:free_seats])
        
        for i, option in enumerate(options):
            out.append({
                **option,
                'postproc': seats_per_quotien[i] + best_r_index[i] if i in best_r_index else seats_per_quotien[i],
            })

        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return Response(out)

    def borda(self, options):

        out = []

        delim=','

        for opt in options:

            lista = opt['option'].split(delim)
            
            out.append({
                **opt,
                'borda': list(enumerate(reversed(lista), 1))[1:],
            })
        
        out.sort(key=lambda x: (-x['votes']))
        return Response(out)

    def sainte_lague(self, options, seats):
        out = []

        options.sort(key=lambda x: -x['votes'])
        for opt in options:
            out.append({
                **opt,
                'postproc': 0,
            })

        for _ in range(seats):

            quotients = []

            for opt in out:
                quotient = opt['votes'] / (2*opt['postproc'] + 1)
                quotients.append(quotient)

            max_value = 0

            for q in quotients:
                if(q > max_value):
                    max_value = q

            index = quotients.index(max_value)

            out[index]['postproc'] += 1
            
        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return Response(out)
    
    def modified_sainte_lague(self, options, seats):
        out = []

        options.sort(key=lambda x: -x['votes'])
        for opt in options:
            out.append({
                **opt,
                'postproc': 0,
            })

        for _ in range(seats):

            quotients = []

            for opt in out:
                if (opt['postproc'] == 0):
                    quotient = opt['votes'] / 1.4
                    quotients.append(quotient)
                
                else:
                    quotient = opt['votes'] / (2*opt['postproc'] + 1)
                    quotients.append(quotient)
                
                
            max_value = 0

            for q in quotients:
                if(q > max_value):
                    max_value = q

            index = quotients.index(max_value)

            out[index]['postproc'] += 1
            
        out.sort(key=lambda x: (-x['postproc'], -x['votes']))
        return Response(out)


    def post(self, request):
        """
         * type: IDENTITY | DHONDT | DROOP | BORDA | HARE | IMPERIALI | REINFORCED_IMPERIAL | HAGENBACH_BISCHOFF | SAINTE_LAGUE | MODIFIED_SAINTE_LAGUE
         * seats: int (just in case type is DHONDT, DROOP, HARE, IMPERIALI, REINFORCED_IMPERIAL, HAGENBACH_BISCHOFF, SAINTE_LAGUE or MODIFIED_SAINTE_LAGUE)
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
        elif t == 'IMPERIALI':
            response = self.imperiali(opts, seats)
        elif t == 'BORDA':
            response = self.borda(opts)
        elif t == 'HARE':
            response = self.hare(opts, seats)
        elif t == 'REINFORCED_IMPERIAL':
            response = self.reinforced_imperial(opts, seats)
        elif t == 'HAGENBACH_BISCHOFF':
            response = self.hagenbach_bischoff(opts, seats)
        elif t == 'SAINTE_LAGUE':
            response = self.sainte_lague(opts, seats)
        elif t == 'MODIFIED_SAINTE_LAGUE':
            response = self.modified_sainte_lague(opts, seats)
        return response
