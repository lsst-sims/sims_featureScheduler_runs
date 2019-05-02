import numpy as np


if __name__ == "__main__":
    # Generate a script to run a grid of basis function weight parameters

    m5ws = [1.]  # One Parameter can be fixed end everything else varried
    footprintws = [.1, 0.5, 1., 3., 10.]
    slewws = [.1, 0.5, 1., 3., 10.]
    fcws = [.1, 0.5, 1., 3., 10.]

    file = open("run_vary_params.script", "w")

    root_path = '/gscratch/astro/yoachim/git_repos/sims_featureScheduler_runs/vary_weights'

    for m5w in m5ws:
        for footprintw in footprintws:
            for sleww in slewws:
                for fcw in fcws:
                    file.write('python %s/vary_weights.py --m5w %f --footprintw %f --sleww %f --fcw %f --outDir %s \n' % (root_path, m5w, footprintw, sleww, fcw, root_path))
file.close()
