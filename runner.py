import simulation
from data import LopezGenerator, GaussianGenerator, DynamicGenerator, TGenerator, SkewedNormGenerator
from model import gHRP, gIVP, gCLA
from util import plotUtil
import numpy as np

'''
    Adding different scenarios to run
    
    Scenario Description:
        1. Name
        2. Parameter Details
        3. Generator

    Synthetic Scenarios
    Things you can vary:
        1. No.of assets
        2. Time horizon of analysis
        3. Underlying return generating process i.e generator
        4. Rebalancing parameter
        5. Exponential weight-decay parameter
        6. Correlators
        7. Linkages for HRP
'''

def generate_basic_scenarios(n,t,corrp):
    '''
    Generates basic scenarios with varying linkages with Lopez generator
    Fixed:
        1. Rebalancing Parameter (l): 22
        2. Exponential weight decay: 0.05
        3. Correlator: Basic correlation
    '''
    pass
    
def run_downturn_scenarios(n_iter,sigma,factor,linkage,n,rholim):
    '''
    Generates basic scenarios with varying linkages.
    Fixed:
        1. Rebalancing Parameter (l): 22
        2. Window = 260.
        3. Correlator: Basic correlation
        4. Underlying return generating process: Dynamic Generator
    Parameters:
        t1: initial period of normal return
        t2: period of downturn
        t3: final period of normal return
    '''
    
    sigma = np.ones(n)*sigma
    mean  = np.zeros(n)
    
    g1 = GaussianGenerator(sigma,mean,'Diagnol',n)
    g2 = GaussianGenerator(sigma*factor,mean,'Correlated',n,rholim)
    
    m = gHRP(linkage_type=linkage)
    m2 = gIVP()
    m3 = gCLA()
    
    datagen = DynamicGenerator(np.array([282,132,146]),[g1,g2,g1],n)
    res = simulation.simulateAll(datagen,[m,m2,m3],22*14,260,22,n_iter)
    
    names = [ name+'__iter_'+str(n_iter)+'__linkage_'+linkage for name in ['HRP','IVP','CLA']]
    
    plotUtil.plot_wts_timeseries(res,names,save_output=True)
    plotUtil.gen_summary_statistics(res,names,save_output=True)


def run_skewedNorm_scenarios(n_iter,sigma,linkage,n,a):
    '''
    Generates basic scenarios with varying linkages.
    Fixed:
        1. Rebalancing Parameter (l): 22
        2. Window = 260.
        3. Correlator: Basic correlation
        4. Underlying return generating process: Dynamic Generator
    Parameters:
        t1: initial period of normal return
        t2: period of downturn
        t3: final period of normal return
    '''
    
    sigma = np.ones(n)*sigma
    mean  = np.zeros(n)
    
    datagen = SkewedNormGenerator(a*np.ones(n),sigma,mean,'CorrelatedGroups',np.array([n//2,n-n//2]),[(0.8,1.0),(0.2,0.4)])
    
    m = gHRP(linkage_type=linkage)
    m2 = gIVP()
    m3 = gCLA()
    
    res = simulation.simulateAll(datagen,[m,m2,m3],22*14,260,22,n_iter)
    
    names = [ name+'__iter_'+str(n_iter)+'__linkage_'+linkage for name in ['HRP','IVP','CLA']]
    
    plotUtil.plot_wts_timeseries(res,names)
    plotUtil.gen_summary_statistics(res,names)

def run_T_scenarios(n_iter,sigma,linkage,n,df):
    '''
    Generates basic scenarios with varying linkages.
    Fixed:
        1. Rebalancing Parameter (l): 22
        2. Window = 260.
        3. Correlator: Basic correlation
        4. Underlying return generating process: Dynamic Generator
    Parameters:
        t1: initial period of normal return
        t2: period of downturn
        t3: final period of normal return
    '''
    
    sigma = np.ones(n)*sigma
    mean  = np.zeros(n)
    
    datagen = TGenerator(df*np.ones(n),sigma,mean,'CorrelatedGroups',np.array([n//2,n-n//2]),[(0.8,1.0),(0.2,0.4)])
    
    m = gHRP(linkage_type=linkage)
    m2 = gIVP()
    m3 = gCLA()
    
    res = simulation.simulateAll(datagen,[m,m2,m3],22*14,260,22,n_iter)
    
    names = [ name+'__iter_'+str(n_iter)+'__linkage_'+linkage for name in ['HRP','IVP','CLA']]
    
    plotUtil.plot_wts_timeseries(res,names,save_output=True)
    plotUtil.gen_summary_statistics(res,names,save_output=True)
    

def run_lopez_replication(n_iter,linkage):
    params = {  'nObs': 520,
                'sLength':260,
                'size0':5,
                'size1':5,
                'mu0':0,
                'sigma0':.01,
                'sigma1F':0.25}
        
    m = gHRP(linkage_type=linkage)
    m2 = gIVP()
    m3 = gCLA()
    
    datagen = LopezGenerator(params['sLength'],params['size0'],params['size1'],params['mu0'],params['sigma0'],params['sigma1F'])
    res = simulation.simulateAll(datagen,[m,m2,m3],22*12,260,22,n_iter)
    
    names = [ name+'__iter_'+str(n_iter)+'__linkage_'+linkage for name in ['HRP','IVP','CLA']]
    
    plotUtil.plot_wts_timeseries(res,names,save_output=True)
    plotUtil.gen_summary_statistics(res,names,save_output=True)
    