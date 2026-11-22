import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from drift import *

def main():
    rng=np.random.default_rng(7);x=rng.normal(size=(37,4));labels=rng.random((20,37))>.3
    actual=randomized_w1(x,labels)
    expected=np.array([[wasserstein_distance(x[l,j],x[~l,j]) for j in range(4)] for l in labels]);assert np.max(np.abs(actual-expected))<1e-12
    x=np.r_[rng.normal(-10,.1,(30,3)),rng.normal(10,.1,(30,3))];assert adjusted_rand_score(np.r_[np.zeros(30),np.ones(30)],kmeans2(x))==1
    g=np.repeat(np.arange(12),3);lab=random_group_labels(g,100,rng);assert all(np.all(lab[:,i:i+3]==lab[:,i,None]) for i in range(0,36,3))
    assert np.all(lab.sum(axis=1)==18)
    pd.DataFrame(dict(test=['exact CDF W1 matches scipy unequal-size samples','NumPy Lloyd recovers separated clusters','randomization preserves whole source groups'],passed=True)).to_csv(OUT/'drift_unit_test_results.csv',index=False)
    print('3 drift numerical checks passed')
if __name__=='__main__':main()
