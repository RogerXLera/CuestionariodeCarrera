# YomaCR
Yoma Course Job Questionnaire for African Youth.
===================
This repository contains the implementation of Course Recommending algorithm for the YOMA project. The data considers a sample of the courses 
offered at the [YOMA platform](https://app.yoma.africa/auth/login). The skills are extracted using the [Skill Extractor](https://lightcast.io/open-skills/extraction) tool offered by
[Lightcast](https://lightcast.io/).
The main developers of this project are Roger X. Lera, [Filippo Bistaffa](https://filippobistaffa.github.io/) and [Juan A. Rodríguez-Aguilar](https://www.iiia.csic.es/~jar/Jariiia/Home.html)

Dependencies
----------
 - [Python 3](https://www.python.org/downloads/)
 - [Pandas](https://pandas.pydata.org/)
 - [Csv library](https://docs.python.org/3/library/csv.html)
 - [Numpy](https://numpy.org/)
 - [CVXPY](https://www.cvxpy.org/)
 - [CPLEX](https://www.ibm.com/es-es/products/ilog-cplex-optimization-studio)

Dataset
----------
Course offered at the [YOMA platform](https://app.yoma.africa/auth/login). The skills are extracted using the [Skill Extractor](https://lightcast.io/open-skills/extraction) tool offered by
[Lightcast](https://lightcast.io/).

Execution
----------
Our approach must be executed by means of the [`solve.py`](solve.py) Python script, i.e.,
```
usage: solve.py [-h] [-m M] [-t T] [--alpha ALPHA] [-p P] [-j J] [-a A] [--name NAME] [--model MODEL] 
                [-- solver SOLVER]

optional arguments:
  -h, --help      show this help message and exit
  -m M            number of time periods (default: 100)
  -t T            tau dedication per period (default: 2)
  --alpha ALPHA   cost function weight parameter (default: 0.5)
  -p P            p-norm (default: 1)
  -j J            job file
  -a A            activities file
  -u U            user pref file
  --name NAME     user name
  --model MODEL   ILP encoding model (choices=['fixed','variable','mixed'])
  --solver SOLVER solver to compute the solution (choices=['CPLEX','GUROBI'])
```

