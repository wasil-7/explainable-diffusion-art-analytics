import sys,unittest,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from features import *
import pandas as pd

class FeatureTests(unittest.TestCase):
    def test_constant(self):
        d,c,e=crop_features(np.full((128,128,3),128,dtype=np.uint8))
        self.assertAlmostEqual(d['H'],0);self.assertAlmostEqual(d['C'],0)
        self.assertEqual(c.sum(),127**2);self.assertEqual(e.sum(),0)
        self.assertAlmostEqual(d['edge_density'],0);self.assertAlmostEqual(d['dwt_LL2'],1)
        self.assertTrue(np.isnan(d['H_no_ties']))
    def test_noise(self):
        rng=np.random.default_rng(42);y=rng.uniform(size=(512,512))
        c,e,t=ordinal_counts(y);h,comp=hc(c)
        self.assertGreater(h,.999);self.assertLess(comp,.002);self.assertEqual(t,0)
        gray=rng.integers(0,256,size=(256,256),dtype=np.uint8)
        d,*_=crop_features(np.repeat(gray[...,None],3,axis=2))
        self.assertLess(abs(d['fft_beta']),.4)
        self.assertAlmostEqual(d['fft_high'],.75,delta=.05)
        # Raw Uniform(0,1) has mean^2=1/4 and variance=1/12.
        # Level1 details each retain (1/4)*(1/12)/(1/3)=1/16.
        self.assertAlmostEqual(d['dwt_HH1'],1/16,delta=.01)
        self.assertAlmostEqual(d['dwt_LL2'],.765625,delta=.02)
    def test_monotone_ramp(self):
        y=np.arange(128*128).reshape(128,128).astype(float)
        c,e,t=ordinal_counts(y);self.assertEqual(np.count_nonzero(c),1);self.assertEqual(hc(c),(0.,0.))
    def test_sinusoid_axes(self):
        x=np.arange(128);w=np.uint8(np.round(127.5+120*np.sin(2*np.pi*x/8)))
        a=np.repeat(np.tile(w,(128,1))[...,None],3,axis=2)
        b=a.transpose(1,0,2)
        da,*_=crop_features(a);db,*_=crop_features(b)
        self.assertGreater(da['dwt_HL1'],da['dwt_LH1']+1e-4)
        self.assertGreater(db['dwt_LH1'],db['dwt_HL1']+1e-4)
        self.assertAlmostEqual(sum(da[f'fft_{i:02d}'] for i in range(16)),1,places=10)
        self.assertAlmostEqual(sum(v for k,v in da.items() if k.startswith('dwt_')),1,places=10)
        peak=max(range(16),key=lambda i:da[f'fft_{i:02d}'])
        self.assertIn(peak,[3,4])
    def test_monochrome(self):
        g=np.arange(128,dtype=np.uint8);im=np.repeat(np.tile(g,(128,1))[...,None],3,axis=2)
        d,*_=crop_features(im)
        self.assertEqual(d['hue_valid'],0);self.assertTrue(np.isnan(d['r_sv']))
        self.assertTrue(np.isnan(d['hue_cos']))
    def test_quadrants_cover_once(self):
        im=np.arange(256*256*3).reshape(256,256,3)
        q=quadrants(im)
        reconstructed=np.concatenate([np.concatenate(q[:2],axis=1),np.concatenate(q[2:],axis=1)],axis=0)
        self.assertTrue(np.array_equal(reconstructed,im))
    def test_point_mass_uniform_bounds(self):
        self.assertEqual(hc(np.array([1]+[0]*23)),(0.,0.))
        h,c=hc(np.ones(24));self.assertAlmostEqual(h,1);self.assertAlmostEqual(c,0)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(FeatureTests);rows=[]
    for test in suite:
        result=unittest.TestResult();start=time.time();test.run(result)
        rows.append(dict(test=test.id(),passed=result.wasSuccessful(),seconds=time.time()-start,details=str(result.errors+result.failures)))
    pd.DataFrame(rows).to_csv(OUT/'unit_test_results.csv',index=False)
    print(pd.DataFrame(rows).to_string(index=False),flush=True)
    sys.exit(0 if all(r['passed'] for r in rows) else 1)
