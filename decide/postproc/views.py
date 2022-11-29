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
    
    def post(self, request):
        """
         * type: IDENTITY | DHONDT | DROOP | REINFORCED_IMPERIAL
         * seats: int (just in case type is DHONDT DROOP OR REINFORCED_IMPERIAL)
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
        elif t == 'REINFORCED_IMPERIAL':
            response = self.reinforced_imperial(opts, seats)

        return response
