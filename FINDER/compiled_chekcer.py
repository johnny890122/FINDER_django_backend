import sys,os
# sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from FINDER import FINDER

if __name__=="__main__":
    dqn = FINDER()
    data = f"../data/empirical/borgatti.gml"
    model = f'../models/Model_EMPIRICAL/911.ckpt'
    val, sol = dqn.Evaluate(data, model)
    print(sol)
    print("done")
