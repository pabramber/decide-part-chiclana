from rest_framework.views import APIView
from rest_framework.response import Response


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

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        return Response({})
