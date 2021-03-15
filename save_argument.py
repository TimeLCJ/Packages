with open(os.path.join(args.output, 'params.sh'), 'w+') as out:
    sys.argv[0] = os.path.join(os.getcwd(), sys.argv[0])
    out.write('#!/bin/bash\n')
    out.write('python3 ')
    out.write(' '.join(sys.argv))
    out.write('\n')