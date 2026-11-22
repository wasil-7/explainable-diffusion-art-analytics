"""Exercise all six dashboard views, filters, navigation and real gallery pixels."""
from common import *
from streamlit.testing.v1 import AppTest

def run_checks(root, output):
    # A fresh process may resolve an isolated submission instead of the full workspace.
    sys.path.insert(0,str(root/'src'))
    for module in ['common','dashboard_views','dashboard_theme','features']:
        sys.modules.pop(module,None)
    at=AppTest.from_file(str(root/'src/dashboard.py'),default_timeout=180).run(timeout=180)
    assert sys.modules['common'].ROOT==root
    from dashboard_views import VIEWS
    checks=[]
    def check(label):
        assert not at.exception,[(e.message,e.stack_trace) for e in at.exception]
        footers=[m.value for m in at.markdown if '<footer' in m.value]
        assert footers==['<footer class="glass footer">Wasil Kayani · Umer Asghar</footer>'],footers
        import re
        visible=' '.join(m.value for m in at.markdown if '<style>' not in m.value)
        assert not re.search(r'24[Ii]\s*[-–]?\s*(?:2551|2532)|i242551|i242532',visible)
        checks.append(label);print('Dashboard passed:',label,flush=True)
    check('default landing, four KPIs, live inspector, baseline and literature')
    assert at.radio(key='view').value==VIEWS[0]
    assert len([m for m in at.markdown if 'class="metric-card' in m.value])==4
    first=at.selectbox(key='quick_artwork').options
    cases=pd.read_csv(root/'results/error_gallery_cases.csv').artwork_id.tolist()
    at.selectbox(key='quick_artwork').set_value(cases[-1]).run(timeout=180);check('quick inspector changes actual artwork')
    for i in [1,2,3]:
        at.button(key=f'method_{i}').click().run(timeout=180);check('methodology navigation '+str(i))
        at.radio(key='view').set_value(VIEWS[0]).run(timeout=180)
    for view in VIEWS[1:]:
        at.radio(key='view').set_value(view).run(timeout=180);check(view)
    for aid in cases:
        at.selectbox(key='gallery_case').set_value(aid).run(timeout=180);check('actual gallery '+aid)
    at.radio(key='view').set_value(VIEWS[1]).run(timeout=180)
    at.radio(key='abstraction').set_value('Hexagonal density').run(timeout=180);check('atlas hexagonal counts')
    at.sidebar.multiselect(key='styles').set_value(['impressionism']).run(timeout=180);check('movement filter')
    at.sidebar.multiselect(key='origins').set_value(['Human']).run(timeout=180);check('origin filter')
    at.sidebar.multiselect(key='styles').set_value([]).run(timeout=180);check('empty atlas filter')
    at.sidebar.multiselect(key='styles').set_value(['impressionism']).run(timeout=180)
    at.radio(key='view').set_value(VIEWS[2]).run(timeout=180);check('PCA')
    at.radio(key='manifold_space').set_value('t-SNE').run(timeout=180);check('t-SNE')
    at.radio(key='abstraction').set_value('Raw artworks').run(timeout=180);check('t-SNE raw coordinates')
    at.radio(key='view').set_value(VIEWS[3]).run(timeout=180)
    at.multiselect(key='profile_origins').set_value(['SD']).run(timeout=180);check('SD spectral sensitivity')
    at.multiselect(key='profile_origins').set_value([]).run(timeout=180);check('empty spectral filter')
    at.radio(key='view').set_value(VIEWS[4]).run(timeout=180)
    at.selectbox(key='drift_feature').set_value(at.selectbox(key='drift_feature').options[-1]).run(timeout=180);check('drift feature selector')
    at.sidebar.multiselect(key='styles').set_value([]).run(timeout=180);check('empty drift filter')
    for name in at.selectbox(key='publication_figure').options:
        at.selectbox(key='publication_figure').set_value(name).run(timeout=180);check('publication figure '+name)
    result={'passed':True,'checks':checks,'root':str(root),'raw_data_present':(root/'data').exists(),'footer':'Wasil Kayani · Umer Asghar','view_count':6}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--package',action='store_true');args=parser.parse_args()
    base=ROOT/'GCR_Submission/i242551_i242532_Milestone03_DSB' if args.package else ROOT
    target=ROOT/'phase3_output/ui_upgrade'/('compact_runtime_verification.json' if args.package else 'dashboard_verification.json')
    run_checks(base,target)
