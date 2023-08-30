Mutual fund matrix completion by IGMC with return prediction
===============================================================================

Methodology
------

This research aims to combine matrix completion approaches with return prediction, which indicates the contribution of matrix completion could achieve for missing data process in the financial area.
The methodology of this research could be divided into three parts:
  1. Matrices accomplishment by matching the time-series data to matrices for NAV, fund flow, and momentum.
  2. Matrix completion approaches performance comparison
  3. Return prediction by FFN and comparison with the performance of missing value process by PCA

### The illustration of methodology 
![methodology](https://github.com/KrisrcQi/Crsp_mutual_fund_matrix_completion/assets/117539900/664d5816-91f7-4eeb-985f-5d20a9ae36cb)

#### The structure of IGMC is based on the approach of Zhang and Chen (2020)
![IGMC applied in mutual fund](https://github.com/KrisrcQi/Crsp_mutual_fund_matrix_completion/assets/117539900/8846ade3-d416-4483-8efa-7bbd3d24e97d)

### The GCN approach is applied to GNN in the IGMC
![GCN](https://github.com/KrisrcQi/Crsp_mutual_fund_matrix_completion/assets/117539900/c59325dc-8b74-47ce-9d18-2005b34c7c77)

### FFN for return prediction 
![FFN](https://github.com/KrisrcQi/Crsp_mutual_fund_matrix_completion/assets/117539900/8e66b59c-6f49-4ea1-b087-67ce5af0460b)
